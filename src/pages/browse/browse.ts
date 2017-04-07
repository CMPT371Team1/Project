import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController, ModalController, ItemSliding, ToastController, Alert} from "ionic-angular";
import {Logger} from "angular2-logger/core";
import {Listing} from "../../app/models/listing";
import {FilterPage} from "../filter/filter";
import {DetailPage} from "../detail/detail";
import {Filter} from "../../app/models/filter";
import {KasperService} from "../../app/providers/kasper-service";
let assert = require('assert-plus');

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html',
    providers: [ListingProvider]
})
export class BrowsePage {
    public static forceRefresh: boolean = true;
    alert: Alert;
    listings: Listing[];
    filter: Filter;

    voteDelay: number = 1000;
    canVote: boolean = true;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                public listingProvider: ListingProvider,
                public modalCtrl: ModalController,
                private _logger: Logger,) {
        this.listings = listingProvider.listings;

        this.filter = new Filter(null, {}, {}, {}, {});
    }

    /**
     * When this tab is opened, reload the listings if it has been requested.
     */
    ionViewDidEnter(){
        if(BrowsePage.forceRefresh) {
            this.loadListings();
            BrowsePage.forceRefresh = false;
        }
    }

    /**
     * Retrieve the listings from the server according to the filter on this page.
     *
     * @post-cond   listings on this page will be overridden with the result
     */
    loadListings(): void{
        let me = this;

        this.listingProvider.getListings(this.filter, ['all'], 5).subscribe(data => {
            me.listings = KasperService.fromData(data['listings']);
        }, error => {
            this.listingProvider.kasperService.handleError("getListings", error.json());
        });
    }

    /**
     * Attempt to retrieve listings from server and get a nolistings error
     *
     */
    loadListingsHook(): void {

        let hook = {"noListingsLeft": "There are no more listings left to view"};

        this.listingProvider.kasperService.handleError("getListings", hook);

    }

    /**
     * Hook to fake no internet access 
     */
    wirelessHook(): void{

        let hook = {"isTrusted": "no'"};

        this.listingProvider.kasperService.handleError("getListings", hook);
    }

    /**
     * Called when the user drags a listing
     *
     * @param event the drag event
     * @param index the index of the listing being dragged
     * @pre-cond    the user has not voted in the last second.
     */
    onDrag(event: ItemSliding, index: number){
        if(!this.canVote) return;
        let me = this;
        if (event.getOpenAmount() < -100) {
            me.likeListing(event, index);
        } else if (event.getOpenAmount() > 100) {
            me.dislikeListing(event, index);
        }
    }

    /**
     * Send request to dislike a listing
     *
     * @param event the event that called this listing
     * @param index the index of the listing
     * @pre-cond    index is not out of bounds
     */
    dislikeListing(event: ItemSliding, index: number): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.startVoteTimer();

        this._logger.debug("Disliking slide at index " + index);

        this.listingProvider.dislikeListing(this.listings[index].listingId).subscribe(data => {
            this.toastCtrl.create({
                message: "Disliked the selected listing.",
                duration: 3000,
                position: 'top'
            }).present();

            this.listings.splice(index, 1);

            if(this.listings.length == 0)
                this.loadListings();
        }, error => {
            if(this.alert) return;


            this.alert = this.listingProvider.kasperService.handleError("likeDislikeListing", error.json());
            this.alert.onDidDismiss(() => {
                event.close();
                this.alert = null;
            });
        });
    }

    /**
     * Send request to like a listing
     *
     * @param event the event that called this listing
     * @param index the index of the listing
     * @pre-cond    index is not out of bounds
     */
    likeListing(event: ItemSliding, index: number): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.startVoteTimer();

        this._logger.debug("Liking slide at index " + index);

        this.listingProvider.likeListing(this.listings[index].listingId).subscribe(data => {
            this.toastCtrl.create({
                message: "Liked the selected listing.",
                duration: 3000,
                position: 'top'
            }).present();

            this.listings.splice(index, 1);

            if(this.listings.length == 0)
                this.loadListings();
        }, error => {
            if(this.alert) return;

            this.alert = this.listingProvider.kasperService.handleError("likeDislikeListing", error.json());
            this.alert.onDidDismiss(() => {
                event.close();
                this.alert = null;
            });
        });
    }

    /**
     * Display the filters screen
     *
     * @post-cond   update the filter on this page if they apply the filter
     */
    goToFilters(): void{
        let me = this;

        let filterModal = this.modalCtrl.create(FilterPage, { filter: this.filter });

        filterModal.onDidDismiss((data: Filter) => {
            if(!data){
                this._logger.debug("Filter Modal was cancelled");
            } else {
                this._logger.debug("Filter Modal Data: " + JSON.stringify(data));
                me.filter = data;
                this.loadListings();
            }
        });

        filterModal.present();
    }

    /**
     * Open the detailed page of a listing
     *
     * @param index the index of the listing
     * @pre-cond    index is not out of bounds
     */
    goToDetails(index): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.navCtrl.push(DetailPage, {data: this.listings, cursor: index});
    }

    /**
     * Set a delay for voting
     */
    startVoteTimer(): void{
        let me = this;
        this.canVote = false;
        setTimeout(function(){
            me.canVote = true;
        }, this.voteDelay);
    }
}
