# API Vulnerability Challenge
## Broken Authentication Challenge
Challenge is present inside the device_registry folder
<ul>
<li>Two users are present, aptly named 'user' and 'admin'</li>
<li>The user credentials will be "leaked" to the contestants</li>
<li>The flag/code can be seen after loggin in as admin</li>
<li>The logic here is to break in via cookies, where the access controls are temporarily stored to distinguish users</li>
<li>Code logic looks at the access-control strings in the cookie and decides the pages to display</li>
</ul>