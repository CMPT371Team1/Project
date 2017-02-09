import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class LoginService {
    data: any;

    constructor(public http: Http) {
        this.data = null;
    }

    login(email: string, password: string): void{

         //POST
        // this.http.post(URL, data, ResponseContentType.Json).subscribe(...)

        //GET
        // this.http.get(URL, ResponseContentType.Json).subscribe(...)

         this.http.post("http://127.0.0.1:8912/signin",
            { email: email, password: password }, ResponseContentType.Json)
             .subscribe(data => {
                this.data = data;
             }, error => {
                 console.log("Oooops, sign in failed!");
             });

    }
}
