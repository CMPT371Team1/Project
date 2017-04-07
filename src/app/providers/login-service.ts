let assert = require('assert-plus');
import {KasperConfig} from "../kasper-config";
import {Injectable} from "@angular/core";
import {SQLite} from "ionic-native";
import "rxjs/add/operator/map";
import {Logger} from "angular2-logger/core";
import {User} from "../models/user";
import {Platform} from "ionic-angular";

/**
 * LoginService holds the current session data of a user, and saves the session data to the device
 * for the app to automatically sign to sign in with later.
 */
@Injectable()
export class LoginService {
    private db: SQLite;

    // The data previously stored in the database
    private userId: number;
    private authToken: string;

    // The user object returned after logging in
    public static user: User;

    constructor(private _logger: Logger,
                private platform: Platform) {
        this.platform.ready().then(() => {
            this.db = new SQLite();

            this.db.openDatabase(KasperConfig.DB_INFO)
                .then(() => {
                    this.loadSessionInfo();
                }, error => {
                    this._logger.error("Could not access database: ");
                    this._logger.error(JSON.stringify(error));
                });
        });
    }

    /**
     * Set the logged in user
     *
     * @param user  the user who is logged in
     *
     * @pre-cond    user is not null
     * @post-cond   the user object is set to user
     * @post-cond   the userId is set to user.id
     */
    public setUser(user: User){
        assert.object(user, "User cannot be null.");

        LoginService.user = user;
        this.userId = user.id;

        assert.equal(LoginService.user, user, "user was not set correctly.");
        assert.equal(this.userId, user.id, "userId was not set correctly.");
    }

    /**
     * Update the auth token for the currently logged in user.
     *
     * @param authToken the new token
     *
     * @pre-cond    authToken is not null
     * @pre-cond    authToken is a string
     * @post-cond   authToken is updated
     * @post-cond   authToken is inserted in the database
     */
    public setToken(authToken: string): void{
        assert(authToken, "The received token was null");
        assert.string(authToken, "The received token was not a string");

        this.authToken = authToken;
        this.updateAuthToken(authToken);

        this._logger.debug("New auth token has been set: " + authToken);
    }

    /**
     * Get the currently logged in user's id
     *
     * @returns {number}    the id
     * @pre-cond    user must be logged in
     */
    public getUserId(): number{
        assert(this.userId, "User must be logged in to get the userId");

        return this.userId;
    }

    /**
     * Get the currently stored authToken
     *
     * @returns {string}    the auth token
     * @pre-cond    user must be logged in
     */
    public getAuthToken(): string{
        assert(this.authToken, "User must be logged in to get the authToken");

        return this.authToken;
    }

    /**
     * Sign the user out of the device
     */
    public signOut(): void{
        LoginService.user = null;
        this.userId = null;
        this.authToken = null;
    }

    /**
     * Insert a new userId/authToken pair into the users.
     *
     * @param authToken the token to insert
     *
     * @pre-cond    LoginService.user is not null
     * @pre-cond    db is not null
     * @post-cond   authToken is inserted in the database
     */
    private updateAuthToken(authToken: string){
        assert.object(LoginService.user, "A user must be logged in to update the auth token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("INSERT INTO session (userId, authToken, created_date) VALUES (?, ?, datetime(now))", [
            this.userId, this.authToken]).then(() => {
            this._logger.debug("New session auth token was saved successfully.");
        }, error => {
            this._logger.error("Could not insert new session auth token: ");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Load the most recent userId and auth token from the users phone.
     *
     * @pre-cond    LoginService.user is not null
     * @pre-cond    db is not null
     * @post-cond   if session info is in the database, it is loaded to userId and authToken.
     */
    private loadSessionInfo(){
        assert.object(LoginService.user, "A user must be logged in to update the auth token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("SELECT userId, authToken FROM session ORDER BY created_date DESC LIMIT 1", {}).then((data) => {
            if(!data.rows) {
                this.userId = data.rows.item(0).userId;
                this.authToken = data.rows.item(0).authToken;
                this._logger.debug(`Loaded previous session info: {userId: ${this.userId}, token: ${this.authToken}`);
            } else {
                this._logger.debug("There was no login session stored on the device");
            }
        }, error => {
            this._logger.error("Error selecting session from SQLite database: ");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Checks whether a user is currently set.
     *
     * @returns {boolean} true if the user is logged in
     */
    public isLoggedIn(): boolean{
        return !!LoginService.user;
    }

}
