export class KasperConfig {
    static DB_INFO: any = {name: "kasper.db", location: 'default'};
    // @if NODE_ENV == 'TEST'
    static API_URL: string = "http://cmpt371g1.usask.ca:4040";
    // @endif


    // @if NODE_ENV == 'DEV'
    static API_URL: string = "http://cmpt371g1.usask.ca:8080";
    // @endif

    static DESIRED_IMAGE_WIDTH: number = 1280;
    static DESIRED_IMAGE_HEIGHT: number = 720;


}
