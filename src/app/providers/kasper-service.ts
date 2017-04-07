import {AlertController} from "ionic-angular";
let assert = require('assert-plus');
import {Injectable} from "@angular/core";
import {Http, ResponseContentType} from "@angular/http";
import {KasperConfig} from "../kasper-config";
import "rxjs/add/operator/map";
import {Logger} from "angular2-logger/core";
import {Filter} from "../models/filter";
import {Listing} from "../models/listing";
import {LoginService} from "./login-service";
import {FormControl} from "@angular/forms";

/**
 * Provides an interface with the API
 */
@Injectable()
export class KasperService {
    public static errorMessages: string[][];

    constructor(public http: Http,
                public loginService: LoginService,
                public alertCtrl: AlertController,
                private _logger: Logger) {
        KasperService.errorMessages = this.initErrors();
    }

    /**
     * Send a login request to the server
     *
     * The return data is as follows
     * {
     *      authToken: string,
     *      userId: int,
     *      email: string,
     *      firstName: string,
     *      lastName: string,
     *      phone1: string,
     *      phone2:string,
     *      city: string,
     *      province: string
     *  }
     *
     * @param email     the email to sign in with
     * @param password  the password to sign in with
     */
    login(email: string, password: string): any{
        let body: FormData = new FormData();
        email = email.replace(' ', '');
        body.append('email', email);
        body.append('password', password);

        return this.http.post(KasperConfig.API_URL + "/signIn", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a login request to the server using a auth token
     *
     * The return data is as follows
     * {
     *      authToken: string
     * }
     */
    loginWithToken(): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/signInToken", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to register the user in the database, then log them in
     *
     * The return data is as follows
     * {
     *      authToken: string,
      *     useId: int
     * }
     *
     * @param email             the email of the user
     * @param password          the desired password
     * @param confirmedPassword the password confirmation
     * @param firstName         the first name of the user
     * @param lastName          the last name of the user
     * @param phone1            primary phone number
     * @param phone2            secondary phone number
     * @param city              the city of the user
     * @param province          abbreviation of province
     */
    signUp(email: string, password: string, confirmedPassword: string, firstName: string,
            lastName: string, phone1: string, phone2: string, city: string, province: string): any{
        let body: FormData = new FormData();
        body.append('email', email);
        body.append('password', password);
        body.append('confirmedPassword', confirmedPassword);
        body.append('firstName', firstName);
        body.append('lastName', lastName);
        body.append('phone1', phone1);
        body.append('phone2', phone2);
        body.append('city', city);
        body.append('province', province);

        return this.http.post(KasperConfig.API_URL + "/createUser", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to update the user's profile
     *
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      firstName, lastName, phone1, phone2, city, province, email
     */
    editUser(changeValues: any): any {
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('changeValues', JSON.stringify(changeValues));

        return this.http.post(KasperConfig.API_URL + "/editUser", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to change the user's password
     *
     * The return data is as follows
     * {
     *      authToken: string
     * }
     *
     * @param oldPassword       the current password of the user
     * @param newPassword       the new password for the user
     * @param confirmedPassword the new password for the user
     */
    changePassword(oldPassword: string, newPassword: string, confirmedPassword: string): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('oldPassword', oldPassword);
        body.append('newPassword', newPassword);
        body.append('confirmedPassword', confirmedPassword);

        return this.http.post(KasperConfig.API_URL + "/changePassword", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Request to sign out of the api.
     */
    signOut(): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/signOut", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Request the favourite listings of a user
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     */
    getFavourites(): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/getFavourites", body,
            ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to like/dislike a listing
     *
     * @param listingId             the listing id
     * @param liked                 do they like it
     */
    likeDislikeListing(listingId: number, liked: boolean): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);
        body.append('liked', liked);

        return this.http.post(KasperConfig.API_URL + "/like", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to get listings according to the specified filter
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     *
     * @param filter            the filter to apply
     * @param valuesRequired    the fields to return about the listings
     * @param maxLimit          the max number of returned results
     */
    getListings(filter: Filter, valuesRequired: string[], maxLimit: number): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('filter', filter.toJson());
        body.append('valuesRequired', JSON.stringify(valuesRequired));
        body.append('maxLimit', maxLimit);

        return this.http.post(KasperConfig.API_URL + "/getListings", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to get listings according to the specified filter
     *
     * The return data is as follows
     * {
     *      myListings: Listing[]
     * }
     *
     */
    getMyListings(): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/getMyListings", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to create a listing
     *
     * The return data is as follows
     * {
     *      listingId: number
     * }
     *
     * @param listing           the listing
     */
    createListings(listing: Listing): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('province', listing.province.abbr);
        body.append('city', listing.city);
        body.append('address', listing.address);
        body.append('price', listing.price);
        body.append('squareFeet', listing.squareFeet);
        body.append('bedrooms', listing.bedrooms);
        body.append('bathrooms', listing.bathrooms);
        body.append('postalCode', listing.postalCode);
        body.append('longitude', 0.0);
        body.append('latitude', 0.0);
        body.append('description', listing.description);
        body.append('images', JSON.stringify(listing.images));
        body.append('thumbnailImageIndex', 0);
        body.append('isPublished', listing.isPublished);

        return this.http.post(KasperConfig.API_URL + "/createListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Delete a listing from the database
     *
     * @param listingId The listing to delete
     */
    deleteListing(listingId: number): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);

        return this.http.post(KasperConfig.API_URL + "/deleteListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to update a listing
     *
     * @param listingId     the listingId to edit
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      province, city, address, price, sqft, bedrooms, bathrooms,
     *                      description, images, thumbnailImageIndex, isPublished
     */
    editListing(listingId: number, changeValues: {}): any {
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);
        body.append('changeValues', JSON.stringify(changeValues));

        return this.http.post(KasperConfig.API_URL + "/editListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to get the contact information for a listing
     *
     * The return data is as follows
     * {
     *       phone1: string,
     *       phone2: string,
     *       email: string
     * }
     *
     * @param listingId     the listing id
     * @param message       the message for the seller
     */
    contactSeller(listingId: number, message: string): any{
        let body: FormData = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);
        body.append('message', message);
        body.append('phone1', LoginService.user.phone1);
        body.append('phone2', LoginService.user.phone2);
        body.append('email', LoginService.user.email);

        return this.http.post(KasperConfig.API_URL + "/requestContactInformation", body
            , ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Appends the userId and authToken to the call if the user is logged in.
     *
     * @param body  the FormData to append to
     */
    appendAuthentication(body: FormData): void{
        if(!this.loginService.isLoggedIn()) return;
        body.append('userId', this.loginService.getUserId());
        body.append('authToken', this.loginService.getAuthToken());
    }

    /**
    * Checks a password for validity.
    *
    * @param c  the form control for the check
    * @returns {strength, message}
    *          strength  the strength of the password [0 to 4]
    *          valid     whether it meets the minimum requirements
    *          message   a message depicting how to raise the strength
    */
    checkPass(c: FormControl): any{
        const requiredStrength: number = 4;

        let lowerCase = new RegExp("^(?=.*[a-z])");
        let upperCase = new RegExp("^(?=.*[A-Z])");
        let numeric = new RegExp("^(?=.*[0-9])");
        let length = new RegExp("^(?=.{8,})");

        if(!lowerCase.test(c.value)){
            return (0 == requiredStrength) ? null : {
                checkPass: {
                    strength: 0,
                    message: "Password must include at least one lower case letter"
                }
            };
        } else if(!upperCase.test(c.value)){
            return (1 == requiredStrength) ? null : {
                checkPass: {
                    strength: 1,
                    message: "Password must include at least one upper case letter"
                }
            };
        } else if(!numeric.test(c.value)){
            return (2 == requiredStrength) ? null : {
                checkPass: {
                    strength: 2,
                    message: "Password must include at least one number"
                }
            };
        } else if(!length.test(c.value)){
            return (3 == requiredStrength) ? null : {
                checkPass: {
                    strength: 3,
                    message: "Password must include at least 8 characters long"
                }
            };
        } else {
            return (4 == requiredStrength) ? null : {
                checkPass: {
                    strength: 4,
                }
            };
        }
    }

    /**
     * Check whether a phone number is valid.
     *
     * @param c the form control for the check
     * @returns null if it is valid or falsey
     *          object otherwise
     */
    checkPhone(c: FormControl): any{
        const numberRegex = new RegExp("^[0-9]{10}$");

        if(!c.value) return null;
        let input = c.value.replace(/[^0-9]*/g, "");

        if(!numberRegex.test(input)){
            return { checkPhone: { valid: false }};
        }

        return null;
    }

    /**
     * Creates the error messages to be displayed when an error is returned from the server.
     *
     * <p>The value held at each route-error pair is the message to be displayed when this error occurs.
     *
     * @returns {string[][]}    a 2D array where the first key is the name of the API route, and the second key is
     *                          the key of the error the server should return.
     */
    initErrors(): string[][]{
        let result: string[][] = [[]];

        result['general'] = [];
        result['general']['isTrusted'] = "There was an error connecting to the server! Please check you're connecting to the internet.";
        result['general']['missingUserId'] = "You must be logged in to do this";
        result['general']['missingToken'] = "You must be logged in to do this";

        result['signIn'] = [];
        result['signIn']['invalidCredentials'] = "Looks like you entered the wrong email or password";
        result['signIn']['missingEmail'] = "Please enter your email to continue";
        result['signIn']['missingPassword'] = "Please enter your password to continue";

        result['signInToken'] = [];
        result['signInToken']['invalidCredentials'] = "Bringing you to the sign in page...";

        result['confirmEmail'] = [];
        result['confirmEmail']['missingUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['confirmEmail']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";

        result['createUser'] = [];
        result['createUser']['emailAlreadyExists'] = "Looks like this email is already in our system";
        result['createUser']['passwordMismatch'] = "Looks like the entered passwords don't match ";
        result['createUser']['passwordNotStrong'] = "Please make sure your password is at least 8 characters long, and has a number and both lower and upper-case characters ";
        result['createUser']['missingEmail'] = "Looks like your email address is missing";
        result['createUser']['missingPassword'] = "Please enter your password";
        result['createUser']['missingConfirmedPassword'] = "Please confirm your password";
        result['createUser']['missingFirstName'] = "Please enter your first name";
        result['createUser']['missingLastName'] = "Please enter your last name";
        result['createUser']['missingPhoneNumber'] = "Please enter your phone number";
        result['createUser']['missingCity'] = "Please enter your city";

        result['deleteListing'] = [];
        result['deleteListing']['invalidListingId'] = "Could not find the listing specified.";
        result['deleteListing']['missingListingId'] = "An error occurred while deleting the listing. (1)";
        result['deleteListing']['invalidUserId'] = "An error occurred while deleting the listing. (2)";

        result['editUser'] = [];
        result['editUser']['emailAlreadyExists'] = "Looks like this email is already in use, please pick a different one";
        result['editUser']['nothingRequestedToChange'] = "If you want to make changes, enter some fields and click save ";
        result['editUser']['unrecognizedKey'] = "Looks like you tried to change a field that doesn't exist. You don't want to do that.";
        result['editUser']['invalidUserId'] = "Setting new information failed.";
        result['editUser']['missingUserId'] = "Setting new information failed. ";
        result['editUser']['passwordCantBeChanged'] = "Please use the change password button to change your password";
        result['editUser']['invalidEmail'] = "The email you entered was invalid";
        result['editUser']['invalidPhone1'] = "The primary phone you entered was invalid";
        result['editUser']['invalidPhone2'] = "The secondary phone you entered was invalid";
        result['editUser']['invalidProvince'] = "The province you entered was invalid";

        result['changePassword'] = [];
        result['changePassword']['missingOldPassword'] = "Please enter your current password";
        result['changePassword']['missingNewPassword'] = "Please enter your new password";
        result['changePassword']['missingNewPasswordConfirmed'] = "Please confirm your now password";
        result['changePassword']['passwordNotStrong'] = "Please make sure your new password is at least 8 characters long, and has a number and both lower and upper-case characters ";
        result['changePassword']['invalidUserId'] = "Setting new password failed.";
        result['changePassword']['missingUserId'] = "Setting new password failed.";
        result['changePassword']['invalidCredentials'] = "Looks like your password was incorrect, please try again";
        result['changePassword']['newPasswordMismatch'] = "Looks like your confirm password didn't match... please try again";
        result['changePassword']['newPasswordIsTheSameAsOld'] = "The new password you entered is the same as your current password. Please choose a new password.";

        result['signOut'] = [];
        result['signOut']['invalidUserId'] = "Looks like you are already signed out";

        result['getFavourites'] = [];
        result['getFavourites']['noFavouriteListing'] = "You don't have anything favourited. To add things to favourites, swipe right on houses on the main page. ";
        result['getFavourites']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['getFavourites']['missingUserId'] = "Something went wrong in the app. We apologize for any inconvenience";

        result['getMyListings'] = [];
        result['getMyListings']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['getMyListings']['missingUserId'] = "Something went wrong in the app. We apologize for any inconvenience";

        result['likeDislikeListing'] = [];
        result['likeDislikeListing']['duplicatedLike'] = "";
        result['likeDislikeListing']['unallowedLiked'] = "You cannot like/dislike your own listing.";
        result['likeDislikeListing']['invalidListingId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['likeDislikeListing']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['likeDislikeListing']['missingUserId'] = "You must be logged in to like or dislike a listing.";
        result['likeDislikeListing']['missingListingId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['likeDislikeListing']['missingLiked'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['likeDislikeListing']['missingToken'] = "You must be logged in to like or dislike a listing.";

        result['getListings'] = [];
        result['getListings']['noListingsLeft'] = "Looks like you've hit the end of your search. To see more listings, adjust your filter settings.";

        result['createListing'] = [];
        result['createListing']['invalidCity'] = "Looks like the city you entered was not recognized";
        result['createListing']['invalidProvince'] = "Looks like the province you entered was not recognized";
        result['createListing']['invalidAddress'] = "Looks like the email address you entered was not recognized";
        result['createListing']['invalidPostalCode'] = "The postal code you entered was invalid";
        result['createListing']['missingPostalCode'] = "A postal code is required";
        result['createListing']['missingImage'] = "At least one image is required to publish a listing";
        result['createListing']['missingAddress'] = "An address is required to publish a listing";
        result['createListing']['missingCity'] = "A city is required to publish a listing";
        result['createListing']['missingDescription'] = "A description is required to publish a listing";

        result['editListing'] = [];
        result['editListing']['nothingRequestedToChange'] = "Make changes, and then click the save button to save them.";
        result['editListing']['unrecognizedKey'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['editListing']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['editListing']['missingUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['editListing']['invalidCredentials'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['editListing']['missingListingId'] = "Something went wrong in the app. We apologize for any inconvenience";

        result['contactSeller'] = [];
        result['contactSeller']['missingListingId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['contactSeller']['missingUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['contactSeller']['invalidUserId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['contactSeller']['invalidListingId'] = "Something went wrong in the app. We apologize for any inconvenience";
        result['contactSeller']['userEmailNotConfirmed'] = "You need to confirm your email before contacting a seller.";

        return result;
    }

    /**
     * Handles errors returned by the Kasper server by displaying an alert message.
     *
     * @param route the api route that the error was returned from
     * @param errors    a dictionary of error keys and messages
     * @returns {Alert} returns a reference to the created Alert
     *
     * @pre-cond    route is not null
     * @pre-cond    errors is not null or empty
     * @post-cond   if the message contained in KasperService.errorMessages is not empty, an alert will be shown.
     */
    handleError(route: string, errors: any) {
        assert(route, "route can not be null");
        assert(errors, "errors can not be null");
        assert(Object.keys(errors).length > 0, "errors can not be empty");

        let firstKey = Object.keys(errors)[0];

        // Check if the error key is in the General declarations
        if(firstKey in KasperService.errorMessages['general']){
            route = "general";
        } else if(!(firstKey in KasperService.errorMessages[route])) {
            this._logger.error("Unhandled error : [" + route + ", " + JSON.stringify(firstKey) + "]");
            return;
        }

        let message: string = KasperService.errorMessages[route][firstKey];

        let alert = this.alertCtrl.create({
            title: "Oops...",
            subTitle: message,
            buttons: ['Dismiss']
        });

        if(message)
            alert.present();

        return alert;
    }

    /**
     * Takes in an object and parses it to a listing object.
     *
     * @param data  the data to parse into Listing objects.
     * @returns {Listing[]} an array of Listings
     *
     * @pre-cond    data is not null
     */
    static fromData(data: any): Listing[]{
        assert(data, "data cannot be null");

        let result: Listing[] = [];

        for(let i=0; i<data.length; i++){
            result.push(
                new Listing(
                    data[i].listingId,
                    data[i].listerId,
                    data[i].bedrooms,
                    data[i].bathrooms,
                    data[i].squareFeet,
                    data[i].price,
                    data[i].description,
                    data[i].isPublished,
                    data[i].createdDate,
                    data[i].modifiedDate,
                    data[i].images,

                    data[i].province,
                    data[i].city,
                    data[i].address,
                    data[i].postalCode,
                    data[i].longitude,
                    data[i].latitude,
                )
            );
        }

        return result;
    }
}
