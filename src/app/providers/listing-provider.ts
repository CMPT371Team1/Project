let assert = require('assert-plus');
import "rxjs/add/operator/map";
import {Injectable} from "@angular/core";
import {Listing} from "../models/listing";
import {Logger} from "angular2-logger/core";
import {Http} from "@angular/http";
import {KasperService} from "./kasper-service";
import {Filter} from "../models/filter";

@Injectable()
export class ListingProvider {
    listings: Listing[];
    myListings: Listing[];

    constructor(public http: Http,
                public kasperService: KasperService,
                private _logger: Logger) {
        this.listings = [];
        this.myListings = [];
    }

    /**
     * Add a listing to the database
     */
    addListing(newListing: Listing): any{
        assert(newListing, "newListing can not be null");

        return this.kasperService.createListings(newListing);
    }

    /**
     * Edit an existing listing in the database
     *
     * @pre-cond    listingId is not null
     */
    editListing(listingId: number, changeValues: {}){
        assert(listingId, "listingId can not be null.");
        this._logger.error("ListingProvider.editListing is not implemented.");
        // return this.kasperService.editListing(listingId, changeValues);
    }

    /**
     * Remove a listing from the database
     *
     * @param listingId the id of the listing
     * @pre-cond    listingId is not null
     */
    removeListing(listingId : number){
        assert(listingId, "listingId can not be null.");
        this._logger.error("ListingProvider.removeListing is not implemented.");
    }

    /**
     * Dislike a listing
     *
     * @param listingId the id of the listing
     * @pre-cond    listingId is not null
     */
    dislikeListing(listingId : number): any{
        assert(listingId, "listingId can not be null.");

        return this.kasperService.likeDislikeListing(listingId, false);
    }

    likeDislikeCallback(){}

    /**
     * Add a listing to a users favourites
     *
     * @param listingId the id of the listing
     * @pre-cond    listingId is not null
     */
    likeListing(listingId : number): any{
        assert(listingId, "listingId can not be null.");

        return this.kasperService.likeDislikeListing(listingId, true);
    }

    /**
     * Remove a listing from a users favourites
     *
     * @param listingId the id of the listing
     */
    removeFromFavourites(listingId : number){
        this._logger.error("ListingProvider.removeFromFavourites is not implemented.");
    }

    /**
     * Search the database according to the specified filter
     *
     * @param filter the filter for the search
     *
     * @return an array of listingIDs
     */
    search(filter : Filter) : any{
        this._logger.error("ListingProvider.search is not implemented.");
        return null;
    }

    /**
     * Get the full information about a listing
     *
     * @param filter            the filter to apply to the search
     * @param requiredFields    the fields we want returned from the server
     * @param limit             the max number of returned results
     * @return a listing
     */
    getListings(filter: Filter, requiredFields: string[], limit: number) : any{
        // If we want all fields
        if(requiredFields.indexOf("all") != -1){
            requiredFields.splice(requiredFields.indexOf("all"), 1);
            requiredFields.push(
                "bedrooms",
                "bathrooms",
                "squareFeet",
                "price",
                "description",
                "isPublished",
                "images",
                "province",
                "city",
                "address",
                "postalCode"
            );
        }
        return this.kasperService.getListings(filter, requiredFields, limit);
    }

    /**
     * Get the full information about a listing
     *
     * @return an array of listings
     */
    getMyListings() : any{
        return this.kasperService.getMyListings();
    }




    /**
     * Get the full information about a listing
     *
     * @return an array of listings
     */
    getFavourites() : any{
        return this.kasperService.getFavourites();
    }

    /**
     * Publish a listing
     *
     * @param listingId the id of the listing
     * @pre-cond    listingId is not null
     */
    publishListing(listingId : number): any{
        assert(listingId, "listingId can not be null");

        return this.editListing(listingId, {'isPublished': true});
    }

    /**
     * Unpublish a listing
     *
     * @param listingId the id of the listing
     * @pre-cond    listingId is not null
     */
    unpublishListing(listingId : number): any{
        assert(listingId, "listingId can not be null");

        return this.editListing(listingId, {'isPublished': false});
    }
}


