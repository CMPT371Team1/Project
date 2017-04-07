import {User} from "../../app/models/user";
import {ChangePasswordPage} from "../change-password/change-password";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {Province} from "../../app/models/province";
import {NavController, ModalController, Platform, AlertController, ToastController} from "ionic-angular";
import {FormGroup, FormBuilder, Validators} from "@angular/forms";
import {LoginService} from "../../app/providers/login-service";
import {SignInPage} from "../sign-in/sign-in";
import {KasperService} from "../../app/providers/kasper-service";
let assert = require('assert-plus');

@Component({
    selector: 'page-my-profile',
    templateUrl: 'my-profile.html'
})
export class MyProfilePage {
    private provinces: Province[];

    profileGroup: FormGroup;

    currentUser: User;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public formBuilder: FormBuilder,
                public toastCtrl: ToastController,
                public alertCtrl: AlertController,
                public kasperService: KasperService,
                public loginService: LoginService,
                public platform: Platform,
                private _logger: Logger) {
        this.loadUser();

        this.provinces = Province.asArray;

        this.profileGroup = this.formBuilder.group({
            email: [null, Validators.compose([Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}")])],
            firstName: [null, Validators.compose([])],
            lastName: [null, Validators.compose([])],
            phone1: [null, Validators.compose([])],
            phone2: [null, Validators.compose([])],
            province: [null, Validators.compose([])],
            city: [null, Validators.compose([])],
            notificationsEnabled: [null, Validators.compose([])],
        });
    }

    /**
     * Set the user object for this page to display
     */
    loadUser(): void{
        assert(LoginService.user, "Tried to load a user but no user was logged in.");

        this.currentUser = LoginService.user;
    }

    /**
     * Display the dialog for the user to update their password.
     *
     * @post-cond   if data is returned, send the request to change the password.
     */
    showChangePassword(): void{
        let changePasswordModal = this.modalCtrl.create(ChangePasswordPage);

        changePasswordModal.onDidDismiss(data => {
            this._logger.debug("Password change was submitted");
            // If the user saves the change
            if(data) {
                this.updatePassword(data.oldPassword, data.newPassword, data.confirmPassword);
            }
        });

        changePasswordModal.present();
    }

    /**
     * Attempt to update the users password in the database.
     *
     * @param currentPassword   users input for their current password
     * @param newPassword       the new password
     * @param confirmedPassword the new password confirmed
     *
     * @pre-cond    no parameters are null
     */
    updatePassword(currentPassword: string, newPassword: string, confirmedPassword: string): void{
        assert(currentPassword, "currentPassword can not be null");
        assert(newPassword, "newPassword can not be null");
        assert(confirmedPassword, "confirmedPassword can not be null");

        let me = this;
        this._logger.debug("Verifying and changing password");

        this.kasperService.changePassword(currentPassword, newPassword, confirmedPassword).subscribe(data => {
            this.alertCtrl.create({
                title: "Success",
                subTitle: "Your password has been changed",
                buttons: ['Dismiss']
            }).present();

            me.loginService.setToken(data.authToken);
        }, error => {
            this.kasperService.handleError("changePassword", error.json());
        });
    }

    getChangedValues(): any{
        let changeValues: {} = {};

        if(this.profileGroup.value.email) changeValues['email'] = this.profileGroup.value.email;
        if(this.profileGroup.value.firstName) changeValues['firstName'] = this.profileGroup.value.firstName;
        if(this.profileGroup.value.lastName) changeValues['lastName'] = this.profileGroup.value.lastName;
        if(this.profileGroup.value.phone1) changeValues['phone1'] = this.profileGroup.value.phone1;
        if(this.profileGroup.value.phone2) changeValues['phone2'] = this.profileGroup.value.phone2;
        if(this.profileGroup.value.province) changeValues['province'] = this.profileGroup.value.province;
        if(this.profileGroup.value.city) changeValues['city'] = this.profileGroup.value.city;

        return changeValues;
    }

    /**
     * Update the users information according to their input
     */
    saveChanges(): void {
        let changeValues: {} = this.getChangedValues();
        console.log(JSON.stringify(changeValues));
        this.kasperService.editUser(changeValues).subscribe(data => {
            let keys = Object.keys(changeValues);

            // update the current user settings to the new values
            for(let i=0; i<keys.length; i++){
                if(keys[i] == "province"){
                    this.currentUser.province = Province.fromAbbr(changeValues[keys[i]]);
                }else{
                    this.currentUser[keys[i]] = changeValues[keys[i]];
                }
            }

        console.log(JSON.stringify(this.currentUser));
            // Clear the form
            this.profileGroup.reset();

            this.alertCtrl.create({
                title: "Success",
                subTitle: "Your changes have been saved",
                buttons: ['Ok']
            }).present();
        }, error => {
            this.kasperService.handleError("editUser", error.json());
        });
    }

    /**
     * Sign the user out of this device.
     */
    signOut(): void{
        let me = this;

        this.kasperService.signOut().subscribe(data => {
            me.loginService.signOut();
            me.navCtrl.setRoot(SignInPage);
            me.navCtrl.parent.select(0);
            me.toastCtrl.create({
                message: "Successfully logged out.",
                duration: 3000,
                position: 'top'
            }).present();
        }, error => {
            this.kasperService.handleError("signOut", error.json());
        });
    }
}
