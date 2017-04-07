import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Loading, LoadingController, NavController, NavParams, ToastController} from 'ionic-angular';
import {Camera} from 'ionic-native';
import {Listing} from "../../app/models/listing";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Province} from "../../app/models/province";
import {KasperConfig} from "../../app/kasper-config";

@Component({
    selector: 'page-add-listing',
    templateUrl: 'add-listing.html',
    providers: [ListingProvider]
})
export class AddListingPage {
    editMode: boolean;

    private _provinces: Province[];

    private listingId: number;
    private listerId: number;
    private modifiedDate: string;
    private createdDate: string;
    private isPublished: boolean;
    private longitude: number;
    private latitude: number;

    bathrooms: number;
    province: string;
    city: string;
    bedrooms: number;
    squareFeet: number;
    price: number;
    address: string;
    postalCode: string;
    description: string;
    images: string[];

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                public loadingCtrl: LoadingController,
                public navParams: NavParams,
                private _logger: Logger) {
        this._provinces = Province.asArray;

        this.images = [];

        if(this.navParams.get('listing')){
            this.loadListingInfo(this.navParams.get('listing'));
            this.editMode = true;
        } else {
            this.loadListingInfo(Listing.emptyListing());
            this.editMode = false;
        }
    }

    /**
     * Move the information from a Listing object into the text areas of this page.
     *
     * @param listing   a listing
     * @pre-cond    listing is not null
     */
    loadListingInfo(listing: Listing): void{
        assert(listing, "listing can not be null");

        this.listingId = listing.listingId;
        this.listerId = listing.listerId;
        this.modifiedDate = listing.modifiedDate;
        this.createdDate = listing.createdDate;
        this.isPublished = listing.isPublished;
        this.longitude = listing.longitude;
        this.latitude = listing.latitude;
        this.bathrooms = listing.bathrooms;
        this.province = listing.province.abbr;
        this.city = listing.city;
        this.bedrooms = listing.bedrooms;
        this.squareFeet = listing.squareFeet;
        this.price = listing.price;
        this.address = listing.address;
        this.postalCode = listing.postalCode;
        this.description = listing.description;
        this.images = listing.images;
    }

    /**
     * Display the UI to add the image
     *
     * @pre-cond    the user give/has given us permission to use the photo library on their device
     * @post-cond   the image is added to the images array
     */
    addImage(){
        const options = {
            // Get image in byte64
            destinationType: 0,//Camera.DestinationType.DATA_URL,
            // Pick image from library
            sourceType: 0,//Camera.PictureSourceType.PHOTOLIBRARY,
            // Dimensions to scale the image to
            targetWidth: KasperConfig.DESIRED_IMAGE_WIDTH, //make it const in kasper config
            targetHeight: KasperConfig.DESIRED_IMAGE_HEIGHT //make it const in kasper config
        };

        Camera.getPicture(options).then((data) => {
            this.images[this.images.length] = data;
        }, (error) => {
            this._logger.error("An error occurred while selecting an image: " + JSON.stringify(error));
        });
    }

    /**
     * Takes the values of the text areas of this page and parses it into a listing.
     *
     * @returns {Listing}   the listing as specified by the user
     */
    getCurListing(): Listing{
        return new Listing(
            this.listingId,
            this.listerId,
            this.bedrooms,
            this.bathrooms,
            this.squareFeet,
            this.price,
            this.description,
            this.isPublished,
            this.createdDate,
            this.modifiedDate,
            this.images,
            this.province,
            this.city,
            this.address,
            this.postalCode,
            this.latitude,
            this.longitude,
        );
    }

    /**
     * Update/Save the listing to the server.
     *
     * @post-cond   if the user is in edit mode, update a listing
     *              if the user is in add mode, create a listing
     */
    saveListing(){
        if(this.editMode){
            this.updateListing();
        } else {
            this.addListing();
        }
    }

    /**
     * Add a new listing to the server, or display an error if the server denies the requset.
     */
    addListing(){
        let loading:Loading = this.loadingCtrl.create({
            content: "Adding Listing..."
        });
        loading.present();

        let result = this.listingProvider.addListing(this.getCurListing());

        result.subscribe(data => {
            this.navCtrl.pop();
            loading.dismiss();
        }, error => {
            loading.dismiss();
            this.listingProvider.kasperService.handleError("createListing", error.json());
        });

    }

    /**
     * Try to add a new listing to the server, the hook listing will give an invalid params error.
     */
    addHookListing(){
        let error = {"invalidPrice": "Price was invalid", "invalidSqft" : "Invalid Square feet"};


        this.listingProvider.kasperService.handleError("createListing", error);


    }

    updateListing(){}

    /**
     * Save the listing to the server without publishing
     */
    saveWithoutPublishing(){
        this.isPublished = false;
        this.saveListing();
    }

    /**
     * Save the listing to the server as a published listing
     */
    saveAndPublish(){
        this.isPublished = true;
        this.saveListing();
    }

    /**
     * Update the listing on the server to be unpublished
     */
    unpublish(){
        this.isPublished = false;
        this.saveListing();
    }
}
