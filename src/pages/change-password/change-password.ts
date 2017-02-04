import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams, NavController, ViewController, AlertController} from 'ionic-angular';

@Component({
    selector: 'page-change-password',
    templateUrl: 'change-password.html'
})
export class ChangePasswordPage {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;

    constructor(public viewCtrl: ViewController,
                params: NavParams,
                private alertCtrl: AlertController,
                private _logger: Logger) {
    }

    passwordsMatch(): boolean{
        return (this.newPassword == this.confirmPassword);
    }

    save(): void{
        if(!this.passwordsMatch()){
            this.alert("Passwords Do Not Match", "The new passwords you entered do not match.");
            return;
        }

        let passwordCheck: any = this.checkPass(this.newPassword);
        if(passwordCheck.strength != 4){
            this.alert("Stronger Password Required", passwordCheck.message);
            return;
        }

        let data = {
            oldPassword: this.currentPassword,
            newPassword: this.newPassword,
        };

        this.viewCtrl.dismiss(data);
    }

    /** Checks a password for validity.
     *
     * @param password  the password to check
     * @precond         the password is not null
     * @returns an object with the following attributes
     *          strength    the strength of the password [0 to 4]
     *          message     a message depicting how to raise the strength
     */
    checkPass(password: string): any{
        assert (password != null);
        let lowerCase = new RegExp("^(?=.*[a-z])");
        let upperCase = new RegExp("^(?=.*[A-Z])");
        let numeric = new RegExp("^(?=.*[0-9])");
        let length = new RegExp("^(?=.{7,})");

        if(!lowerCase.test(password)){
            return {
                strength: 0,
                message: "Password must include at least one lower case letter"
            };
        }
        if(!upperCase.test(password)){
            return {
                strength: 1,
                message: "Password must include at least one upper case letter"
            };
        }
        if(!numeric.test(password)){
            return {
                strength: 2,
                message: "Password must include at least one number"
            };
        }
        if(!length.test(password)){
            return {
                strength: 3,
                message: "Password must include at least 7 characters long"
            };
        }
        return {
            strength: 4
        };
    }

    cancel(): void{
        this.viewCtrl.dismiss();
    }

    alert(title: string, message: string){
        this.alertCtrl.create({
            title: title,
            subTitle: message,
            buttons: ["Ok"]
        }).present();
    }
}
