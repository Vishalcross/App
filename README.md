# API Vulnerability Challenge
## Broken Authentication Challenge
Challenge is present inside the AuthN folder
<ul>
<li>Start the challenge by starting docker and then building and running it
<li>Challenge is hosted at http://localhost:5000</li>
<li>Two users are present, aptly named 'user' and 'admin'</li>
<li>The user credentials will be "leaked" to the contestants</li>
<li>The flag/code can be seen after loggin in as admin</li>
<li>The logic here is to break in via cookies, where the access controls are temporarily stored to distinguish users</li>
<li>Code logic looks at the access-control strings in the cookie and decides the pages to display</li>
</ul>

## Object Level Broken Authorization Challenge
**Challenge is present inside the AuthZ folder**

- Three users are present, user1,user2 and user3
- The user1 credentials will be given to the contestants
- Upon login the username will  be redirected '/user/username' endpoint
- The contestant need to type the url '/user/user2' to find the flag

