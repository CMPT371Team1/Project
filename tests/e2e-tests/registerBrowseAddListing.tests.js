describe('Registering new user as a user would', function() {
    let originalTimeout;
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        sleep();
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 100000; //100 seconds

    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    it('Should register', function(done){

        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click();
        sleep();

        let registerButton;
        registerButton = element(by.css('.register'));
        registerButton.click();
        sleep();

        let email, password, confirmPassword;
        email = element(by.id('signUpEmail')).all(by.tagName('input')).first();
        password = element(by.id('signUpPassword')).all(by.tagName('input')).first();
        confirmPassword = element(by.id('signUpConfirmPassword')).all(by.tagName('input')).first();

        let nextButton;
        nextButton = element(by.buttonText('Next'));


        email.sendKeys('wrongFormatEmail');
        password.sendKeys('Password123');
        confirmPassword.sendKeys('Password123');
         nextButton.click();
        email.sendKeys().clear();
        password.sendKeys().clear();
        confirmPassword.sendKeys().clear();
        email.sendKeys('chrismIsTheBest@email.ca');
        password.sendKeys('weakpassword');
        confirmPassword.sendKeys('weakpassword');
         nextButton.click();
        password.sendKeys().clear();
        confirmPassword.sendKeys().clear();
        password.sendKeys('NotMatchingPassword123');
        confirmPassword.sendKeys('DifferentPassword123');
         nextButton.click();
        password.sendKeys().clear();
        confirmPassword.sendKeys().clear();
        password.sendKeys('Password123');
        confirmPassword.sendKeys('Password123');
         nextButton.click();

        sleep();

        let firstName, lastName, phoneNumber;
        nextButton = element(by.buttonText('Next'));
        firstName = element(by.id('signUpFirstName')).all(by.tagName('input')).first();
        lastName = element(by.id('signUpLastName')).all(by.tagName('input')).first();
        phoneNumber = element(by.id('signUpPhoneNumber')).all(by.tagName('input')).first();
        firstName.sendKeys('John');
        lastName.sendKeys('Smith');
        // test with too long of phoneNumber
        phoneNumber.sendKeys('30655512341234');
        nextButton.click();
        phoneNumber.sendKeys().clear();
        // test with too short of phoneNumber
        phoneNumber.sendKeys('306555');
        nextButton.click();
        phoneNumber.sendKeys().clear();
        // test with letters
        phoneNumber.sendKeys("phoneNumbr");
        nextButton.click();
        phoneNumber.sendKeys().clear();
        // correct format
        phoneNumber.sendKeys("3065551234");

        nextButton.click();
        sleep();

        let province, city, ABoption;

        province = element(by.id('signUpProvinceSelect')).click();
        sleep();
        ABoption = element(by.buttonText('Alberta'));
        ABoption.click();
        sleep();
        let okButton;
        okButton = element(by.buttonText('OK'));
        okButton.click();
        sleep();
        city = element(by.id('signUpCity')).all(by.tagName('input')).first();
        city.sendKeys('Edmonton');


         let finish = element(by.buttonText('Finish'));
         finish.click();

        // if still on register then go back to login and login with same username as this email has
        // already been registered in the database
        // else continue with my profile
       /* if(finish.isDisplayed()){
            myProfileTab.click();
            sleep();
            email = element(by.id('email')).all(by.tagName('input')).first();
            password = element(by.id('password')).all(by.tagName('input')).first();
            let signInButton = element(by.buttonText('Sign In'));
            email.sendKeys('test@usask.ca');
            password.sendKeys('wrongPassword123');
             signInButton.click();
            password.sendKeys().clear();
            password.sendKeys('Password123');
            signInButton.click();
            sleep();

        }*/

        finish.isPresent().then(function(present) {
          if (present) {
                        myProfileTab.click();
                        sleep();
                        email = element(by.id('email')).all(by.tagName('input')).first();
                        password = element(by.id('password')).all(by.tagName('input')).first();
                        let signInButton = element(by.buttonText('Sign In'));
                        email.sendKeys('test1@test.com');
                        //TODO Fix to accomodate new sign-in error prompt
                        //password.sendKeys('wrongPassword123');
                        //signInButton.click();
                        //password.sendKeys().clear();
                        password.sendKeys('123abcABC');
                        signInButton.click();
                        sleep();
          } else {
            //
          }
        });

        done();
     });

    //TODO Fix to accomodate Browse Page changes
    /*
    it('Should browse listings', function(done){

        let browseButton = element(by.id('tab-t0-0'));
        browseButton.click();
        sleep();

        let browseImage;
        browseImage = element(by.id('image'));
        // drag and drop not working
       // browser.actions().dragAndDrop(browseImage,{x:50,y:0}).perform();
        browseImage.click();
        sleep();
        let rightArrowButton = element(by.id('nextProperty'));
        let leftArrowButton = element(by.id('previousProperty'));
        let likeButton = element(by.id('likeButton'));
        let unlikeButton = element(by.id('unlikeButton'));
        let description = element(by.id('description'));

        for(i=0; i<5; i++)
                 {
                    try{
                     rightArrowButton.click();
                     if(i%2 == 0)
                     {
                         browser.executeScript("arguments[0].scrollIntoView();", description);
                         sleep();
                         browser.executeScript("arguments[0].scrollIntoView();", likeButton);
                         likeButton.click();
                     }
                     else
                     {
                        unlikeButton.click();
                     }
                     }
                     catch(NoSuchElementError){
                        console.err("ran out of listings to browse");
                     }
                 }
        done();

     });
     */

    it('Should add listing', function(done){

        //go to myListings tab
        let myListings = element(by.id('tab-t0-3'));
        myListings.click();
        sleep();

        //go to the addListings screen
        let addListingButton= element(by.id('addButton'));
        addListingButton.click().then(function(){
            //filter options
            let provinceDropList = element(by.id('alProvince'));
            // .all(by,tageName ('')).first() is needed to input text into the text box
            let bath = element(by.id('alBathroom')).all(by.tagName('input')).first();
            let city = element(by.id('alCityTown')).all(by.tagName('input')).first();
            let address = element(by.id('alAddress')).all(by.tagName('input')).first();
            let postalCode = element(by.id('alPostalCode')).all(by.tagName('input')).first();
            let price = element(by.id('alPrice')).all(by.tagName('input')).first();
            let feet = element(by.id('alSqft')).all(by.tagName('input')).first();
            let bed = element(by.id('alBedroom')).all(by.tagName('input')).first();
            let desc2 = element(by.id('alDesc')).all(by.tagName('textarea')).first();

            //save button
            let saveButton = element(by.id('alSave'));

            //open province drop down
            sleep();
            provinceDropList.click().then(function(){
                let skOption = element(by.buttonText('Saskatchewan'));
                let OKbtn = element(by.buttonText('OK'));
                //select SK and press OK
                browser.executeScript("arguments[0].scrollIntoView();", skOption).then(function(){
                    sleep();
                    skOption.click();
                    sleep();
                    OKbtn.click();
                });
            });
            city.sendKeys('Saskatoon');
            address.sendKeys('123 First Street East');
            postalCode.sendKeys('f1s 9u8');

            browser.executeScript("arguments[0].scrollIntoView();", bath); //scroll into view

            price.sendKeys('13000000');
            feet.sendKeys('600');
            bed.sendKeys('5');
            bath.sendKeys('2');
            desc2.sendKeys('Nice trailer with a little dust. Fixer Upper.');

            //submit listing
            saveButton.click();
        });




        sleep();
        //TODO: add expect
        done();

    });

    function sleep(){
        browser.driver.sleep(500)
    }

});
