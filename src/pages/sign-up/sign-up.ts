import {Component, ViewChild} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {NavController, ToastController, Slides, Platform} from "ionic-angular";
import {KasperService} from "../../app/providers/kasper-service";
import {FormGroup, FormBuilder, Validators} from "@angular/forms";
import {MyProfilePage} from "../my-profile/my-profile";
import {Province} from "../../app/models/province";
import {User} from "../../app/models/user";
let assert = require('assert-plus');

@Component({
    selector: 'page-sign-up',
    templateUrl: 'sign-up.html',
    providers: [KasperService]
})
export class SignUpPage {
    private _provinces: Province[];
    step: number;

    // Form validation
    signUpStep1: FormGroup;
    private emailAttempted: boolean = false;
    private passwordAttempted: boolean = false;
    private confirmPasswordAttempted: boolean = false;

    signUpStep2: FormGroup;
    private firstNameAttempted: boolean = false;

    signUpStep3: FormGroup;

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public formBuilder: FormBuilder,
                public toastCtrl: ToastController,
                public kasperService: KasperService,
                public platform: Platform) {

        this.step = 1;

        this._provinces = Province.asArray;

        // Create validation for step 1
        this.signUpStep1 = formBuilder.group({
            email: [null, Validators.compose([Validators.required,
                Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}")])],
            password: [null, Validators.compose([Validators.required, kasperService.checkPass])],
            confirmPassword: [null, Validators.compose([Validators.required])],
        });

        // Create validation for step 2
        this.signUpStep2 = formBuilder.group({
            firstName: [null, Validators.compose([Validators.required])],
            lastName: ['', Validators.compose([])],
            phoneNumber: ['', Validators.compose([kasperService.checkPhone])],
        });

        // Create validation for step 3
        this.signUpStep3 = formBuilder.group({
            province: ['', Validators.compose([Validators.required])],
            city: ['', Validators.compose([])],
        });
    }

    /**
     * Send the request to the server to register a new user
     *
     * @post-cond   if there was no error from the server, log the user in and move them to the browse screen,
     *              otherwise display an error
     */
    doRegister(): void{
        let result = this.kasperService.signUp(this.signUpStep1.value.email,
                                this.signUpStep1.value.password,
                                this.signUpStep1.value.confirmPassword,
                                this.signUpStep2.value.firstName,
                                this.signUpStep2.value.lastName,
                                this.signUpStep2.value.phoneNumber,
                                "", // phone2
                                this.signUpStep3.value.city,
                                this.signUpStep3.value.province);

        let user: User = new User(-1, this.signUpStep1.value.email, this.signUpStep2.value.firstName,
            this.signUpStep2.value.lastName, this.signUpStep2.value.phoneNumber, "",
            Province.fromAbbr(this.signUpStep3.value.province),
            this.signUpStep3.value.city);

        this.registerCallback(result, user);
    }

    /**
     * Handle the data from the register request
     *
     * @param data  the data returned from the request
     * @param user  the user object sent with the request
     */
    registerCallback(data: any, user: User){
        data.subscribe(data => {
            user.id = data.userId;
            this.kasperService.loginService.setUser(user);
            this.kasperService.loginService.setToken(data.authToken);

            this.navCtrl.setRoot(MyProfilePage);

            this.toastCtrl.create({
                message: "Registered successfully.",
                duration: 3000,
                position: 'top'
            }).present();

            // Move back to the browse page.
            // This is currently required as selecting the My Profile tab a second time (before
            // changing to another tab) will bring the user back to the SignInPage page.
            this.navCtrl.parent.select(0);
        }, error => {
            this.kasperService.handleError("signUp", error.json());
        });
    }

    /**
     * Go to the next step if the fields are valid
     *
     * @pre-cond    the current step passed validation
     * @pre-cond    there is a next step
     * @post-cond   step is incremented or we register if we are on the last step
     */
    nextStep(): void{
        if(this.confirmStep()){
            if(this.step != 3) {
                this.step++;
            } else {
                this.doRegister();
            }
        } else {
            this.attemptAll();
            this.toastCtrl.create({
                message: "Please validate fields before continuing.",
                duration: 3000,
                position: 'top'
            }).present();
        }
    }

    /**
     * Move back to the previous step.
     *
     * @pre-cond    there is a previous step
     * @post-cond   step is decremented
     */
    previousStep(): void{
        if(this.step != 1) {
            this.step--;
        }
    }

    /**
     * Confirm the validity of the current step
     *
     * @returns {boolean}   true if the fields are valid
     *                      false otherwise
     * @pre-cond    the current step index exists
     */
    confirmStep(): boolean {
        switch (this.step) {
            case 1:
                return (this.signUpStep1.valid &&
                this.signUpStep1.value.password == this.signUpStep1.value.confirmPassword);
            case 2:
                return this.signUpStep2.valid;
            case 3:
                return this.signUpStep3.valid;
            default:
                assert(false, "Tried to confirm step that did not exist.");
        }
    }

    // The following functions update variables that toggle the display of error messages
    attemptAll(){
        if(this.step == 1) {
            this.attemptEmail();
            this.attemptPassword();
            this.attemptConfirmPassword();
        } else if (this.step == 2){
            this.attemptFirstName();
        } else if (this.step == 3){

        }
    }

    attemptEmail(){
        this.emailAttempted = true;
    }

    attemptPassword(){
        this.passwordAttempted = true;
    }

    attemptConfirmPassword(){
        this.confirmPasswordAttempted = true;
    }

    attemptFirstName(){
        this.firstNameAttempted = true;
    }
}
