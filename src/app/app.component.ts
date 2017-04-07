import {Component} from "@angular/core";
import {Platform} from "ionic-angular";
import {StatusBar, Splashscreen, SQLite} from "ionic-native";
import {KasperConfig} from "./kasper-config";
import {Logger} from "angular2-logger/core";
import {MainPage} from "../pages/main/main";
let assert = require('assert-plus');

@Component({
    templateUrl: 'app.html'
})
export class MyApp {
    rootPage = MainPage;

    constructor(platform: Platform,
                private _logger: Logger) {

        platform.ready().then(() => {
            let db = new SQLite();

            db.openDatabase(KasperConfig.DB_INFO).then(() => {
                this.createLoginTable(db);
            }, error => {
                this._logger.error("Could not access SQLite database: ");
                this._logger.error(JSON.stringify(error));
            });
        });

        StatusBar.styleDefault();
        Splashscreen.hide();
    }

    /**
     * Creates the table containing the user's session info.
     *
     * @pre-cond    db is not null
     * @param db  an open SQLite connection
     */
    private createLoginTable(db: SQLite): void {
        assert(db, "db can not be null");

        db.executeSql(
            "CREATE TABLE IF NOT EXISTS session(" +
            "userId       INT PRIMARY KEY, " +
            "authToken    VARCHAR(255), " +
            "created_date DATETIME)", {})
            .then(() => {
                // Don't do anything if it's created successfully or already exists.
            }, error => {
                this._logger.error("Could not create session table: ");
                this._logger.error(JSON.stringify(error));
            });
    }
}
