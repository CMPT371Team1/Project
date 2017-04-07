import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {
    NavController, ToastController, ViewController, LoadingController,
    Loading, AlertController
} from "ionic-angular";
import {SignUpPage} from "../sign-up/sign-up";
import {KasperService} from "../../app/providers/kasper-service";
import {User} from "../../app/models/user";
import {Province} from "../../app/models/province";
import {MyProfilePage} from "../my-profile/my-profile";
import {BrowsePage} from "../browse/browse";
let assert = require('assert-plus');

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html',
    providers: [KasperService]
})
export class SignInPage {
    loginForm: FormGroup;
    private emailAttempted: boolean = false;

    private loading: Loading;

    constructor(public navCtrl: NavController,
                public alertCtrl: AlertController,
                private _logger: Logger,
                public loadingCtrl: LoadingController,
                public formBuilder: FormBuilder,
                public kasperService: KasperService) {
        this.loginForm = formBuilder.group({
            email: ['', Validators.compose([Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}"), Validators.required])],
            password: ['', Validators.compose([Validators.required])],
        });
    }

    /**
     * Switch the user to the sign up screen.
     */
    pushRegister(): void{
        this._logger.debug("Register was clicked.");
        this.navCtrl.push(SignUpPage);
    }

    /**
     * Attempt to log the user in with the provided information
     *
     * @post-cond   if there was no error, log the user in and move them to the browse screen, otherwise display an
     *              error
     */
    doSignIn(): void{
        this._logger.debug("Sign In was clicked.");

        if(this.loginForm.valid){
            let result = this.kasperService.login(this.loginForm.value.email, this.loginForm.value.password);

            this.loading = this.loadingCtrl.create({
                content: "Logging in..."
            });
            this.loading.present();

            this.signInCallback(result);
        } else {
            this._logger.error("Tried to submit when fields do not pass validation.");
        }
    }

    facebookLogin(): void{}

    /**
     * Handle data from the login request
     *
     * @param result the response from the server
     */
    signInCallback(result: any): void{
        result.subscribe(data => {
            // Create a user object from the result of the login statement
            let user: User = new User(data.userId, data.email, data.firstName, data.lastName,
                data.phone1, data.phone2, Province.fromAbbr(data.province), data.city);

            // Set the login data for the user
            this.kasperService.loginService.setUser(user);
            this.kasperService.loginService.setToken(data.authToken);

            // Set the root of the current tab to the MyProfile page.
            this.navCtrl.setRoot(MyProfilePage);

            BrowsePage.forceRefresh = true;

            // Move back to the browse page.
            // This is currently required as selecting the My Profile tab a second time (before
            // changing to another tab) will bring the user back to the SignInPage page.
            this.navCtrl.parent.select(0);

            }, error => {
                this.kasperService.handleError("signIn", error.json());
            });
        this.loading.dismiss();
    }

    /**
     * Mark the email field as attempted so errors will show up if it is invalid
     */
    attemptEmail(){
        this.emailAttempted = true;
    }
}
