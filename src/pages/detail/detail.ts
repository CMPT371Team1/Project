import {ListingProvider} from "../../app/providers/listing-provider";
import {Component, ViewChild} from "@angular/core";
import {NavController, ModalController, NavParams, Slides, ToastController} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {LoginService} from "../../app/providers/login-service";
import {AddListingPage} from "../add-listing/add-listing";
import {ContactPage} from "../contact/contact";
let assert = require('assert-plus');

@Component({
    selector: 'page-detail',
    templateUrl: 'detail.html',
    providers: [ListingProvider]
})
export class DetailPage {
    @ViewChild(Slides) slides: Slides;
    data: Listing[];
    cursor: number = 0;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public toastCtrl: ToastController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger,
                public navParams: NavParams) {
        this.data = navParams.get('data');
        this.cursor = navParams.get('cursor');
    }

    /**
     * Add the house to the users dislike list
     */
    dislike(): void{
        this.toastCtrl.create({
            message: "Disliked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();
        this.listingProvider.dislikeListing(this.data[this.cursor].listingId).subscribe(data => {
            this._logger.debug("Dislike was successful.");
        }, error => {
            this.listingProvider.kasperService.handleError("likeDislikeListing", error.json());
        });
    }

    /**
     * dislike test hook attempt to dislike a house get invalid userid error
     */
    dislikeHook(): void{
        let error = {"invalidUserId" : "invalid user id"};

        this.listingProvider.kasperService.handleError("likeDislikeListing", error);
    }

    /**
     * like test hook attempt to dislike a house get invalid userid error
     */
    likeHook(): void {
        let error = {"invalidUserId": "invalid user id"};

        this.listingProvider.kasperService.handleError("likeDislikeListing", error);
    }

    /**
     * Add the house to the users favourites list
     */
    like(): void{
        this.toastCtrl.create({
            message: "Liked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();
        this.listingProvider.likeListing(this.data[this.cursor].listingId).subscribe(data => {
            this._logger.debug("Like was successful.");
        }, error => {
            this.listingProvider.kasperService.handleError("likeDislikeListing", error.json());
        });
    }

    /**
     * Return to the first image in the slides
     */
    goToFirstSlide(): void{
        assert(this.slides, "slides can not be null");

        this.slides.slideTo(0, 0);
    }

    /**
     * Display the next property
     *
     * @pre-cond    there is a next property available
     */
    nextProperty(): void{
        this.goToFirstSlide();

        if(this.isNextProperty())
            this.cursor += 1;
    }

    /**
     * Display the previous property
     *
     * @pre-cond    there is a previous property available
     */
    previousProperty(): void{
        this.goToFirstSlide();

        if(this.isPreviousProperty())
            this.cursor -= 1;
    }

    /**
     * Edit the current property
     */
    edit(): void{
        this.navCtrl.push(
            AddListingPage, { listing: this.data[this.cursor] }
        );
    }

    /**
     * Check if there is a property before the current.
     *
     * @returns {boolean}   true if there is a property before this one
     */
    isPreviousProperty(): boolean{
        return this.cursor > 0;
    }

    /**
     * Check if there is a property after the current.
     *
     * @returns {boolean}   true if there is a property afterhis one
     */
    isNextProperty(): boolean{
        return this.cursor < (this.data.length - 1);
    }

    /**
     * Check if the current property belongs to the logged in user
     *
     * @returns {boolean}   true if it is their property
     */
    belongsToUser(): boolean{
        if(!this.loginService.isLoggedIn())
            return false;

        return this.loginService.getUserId() == this.data[this.cursor].listerId;
    }

    /**
     * Display the contact page for the user who created the current property
     */
    goToContact(): void{
        this.navCtrl.push(ContactPage, {listingId: this.data[this.cursor].listingId});
    }
}
