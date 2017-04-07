import {LoginService} from "../../app/providers/login-service";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController, ModalController, ToastController} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {DetailPage} from "../detail/detail";
import {AddListingPage} from "../add-listing/add-listing";
import {KasperService} from "../../app/providers/kasper-service";
let assert = require('assert-plus');

@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [ListingProvider]
})
export class MyListingsPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger) {

        this.listings = Array();
    }

    /**
     * Refresh the users listings when they open this tab
     *
     * TODO make this more efficient
     */
    ionViewDidEnter(){
        let me = this;

        if(this.loginService.isLoggedIn()) {
            this.listingProvider.getMyListings().subscribe(data => {
                me.listings = KasperService.fromData(data['listings']);
            }, error => {
                this._logger.error(JSON.stringify(error));
            });
        } else {
            this.listings = Array();
        }
    }

    /**
     * Display the detailed view for the selected listing
     *
     * @param listing listing clicked by user
     * @pre-cond    listing is not null
     */
    selectListing(listing:Listing){
        assert(listing, "listing can not be null");

        this.navCtrl.push(DetailPage, {
            data: this.listings,
            cursor: this.listings.indexOf(listing)
        });
        this._logger.debug("ListingId  " + listing + " was clicked"); //probably changed to listing id and semicolon
    }

    /**
     * Display the edit listing view for the selected listing
     *
     * @param listing: listing to be edited
     * @pre-cond    listing is not null
     */
    editListing(listing:Listing){ //add asserts to methods
        assert(listing, "listing can not be null");

        this.navCtrl.push(AddListingPage,{ //add comment to explain that addListingPage is the same as edit...
            listing: listing
        });

    };

    /**
     * Delete a listing from the users listings
     *
     * @param listing: listing to be deleted
     * @pre-cond    listing is not null
     */
    deleteListing(listing:Listing){
        assert(listing, "listing can not be null");

        this.listingProvider.kasperService.deleteListing(listing.listingId).subscribe(result => {
            let selectedIndex = this.listings.indexOf(listing);
            this.listings.splice(selectedIndex, 1);

            this.toastCtrl.create({
                message: "The listing has been deleted",
                duration: 3000,
                position: 'top'
            }).present();
        }, error => {
            this.listingProvider.kasperService.handleError("deleteListing", error.json());
        });
    }

    /**
     * Hook for deleteListing. The error it repuclates is invalid userid
     */
    deleteListingHook(listing:Listing){
        assert(listing, "listing can not be null");

        let error = {"invalidUserId" : "invalid user id"};

        this.listingProvider.kasperService.handleError("deleteListing", error);
    }

    /**
     * Display the add listing page.
     *
     * @pre-cond    the user is logged in
     */
    addListing(){
        if(!this.loginService.isLoggedIn()) return;

        this.navCtrl.push(AddListingPage);
    }

    /**
     * Get the unpublished listings from the listings loaded on this page.
     *
     * @returns {Listing[]}  the unpublished listings
     */
    getUnpublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(!this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }

    /**
     * Get the published listings from the listings loaded on this page.
     *
     * @returns {Listing[]}  the published listings
     */
    getPublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }
}
