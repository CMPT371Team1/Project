beforeEach(function () {
    originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
    jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds

});

afterEach(function() {
    jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
});

    describe('Browsing listings as a user would', function() {
        let originalTimeout;
        browser.get('/#/ionic-lab');

    it('Should browse listings', function(done){
        sleep();
        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click().then(function(){
                    let signInButton = element(by.buttonText('Sign In'));
                    checkDisplayed(signInButton, "The 'Sign In' page ");

        });
        //myProfileTab.click();
        //sleep();

        attemptSignIn('test1@test.com', '123abcABC');
        sleep();

        let browseButton = element(by.id('tab-t0-0'));
        browseButton.click();
        sleep();

        let browseImage = element(by.id('image'));
        browseImage.click();
        sleep();
        let rightArrowButton = element(by.id('nextProperty'));
        let leftArrowButton = element(by.id('previousProperty'));
        let likeButton = element(by.id('likeButton'));
        let unlikeButton = element(by.id('unlikeButton'));
        let description = element(by.id('description'));

        for(i=0; i<3; i++)
                 {
                    try{
                        sleep();
                     rightArrowButton.click();
                     if(i%2 == 0)
                     {
                         browser.executeScript("arguments[0].scrollIntoView();", description);
                         sleep();
                         browser.executeScript("arguments[0].scrollIntoView();", likeButton);
                        // likeButton.click();
                     }
                     else
                     {
                       // unlikeButton.click();
                     }
                     }
                     catch(NoSuchElementError){
                        console.err("ran out of listings to browse");
                     }
                 }
        done();

     });
});


/**
 * Force the browser to sleep for a specified amount of time.
 * @param {number} time - The amount of time to sleep (in milliseconds)
 */
function sleep(){
    browser.driver.sleep(1000);
}

/**
 * Check if the input value was entered properly.
 * @param {element} element - The element with the value.
 * @param {string} expectedValue - The expected value that should be contained in the element input.
 */
function checkAttribute(element, expectedValue){
    expect(element.getAttribute('value')).toContain(expectedValue);
}

/**
 * Check if the element is currently being displayed.
 * @param {element} element - The element to check.
 * @param {string} item - The item that should be displayed.
 */
function checkDisplayed(element, item){
    expect(element.isDisplayed()).toBe(true, "Expected " + item + " to be displayed, but was not");
}

/**
* Try to sign in with the expectation of a correct username and password
* @param {string} emailInput - the email field to input
* @param {string} passwordInput - the password field to input
*/
function attemptSignIn(emailInput, passwordInput){
    let email = element(by.id('email')).all(by.tagName('input')).first();
    let password = element(by.id('password')).all(by.tagName('input')).first();
    let signInButton = element(by.buttonText('Sign In'));

    email.sendKeys().clear();
    password.sendKeys().clear();
    email.sendKeys(emailInput);
    password.sendKeys(passwordInput);
    signInButton.click();

}
