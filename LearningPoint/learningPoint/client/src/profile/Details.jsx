import React, {useState} from 'react';
import { Link } from 'react-router-dom';

import { accountService } from '@/_services';

function facultyCheck(check){
    if (check){
        return "Tutor";
    }
    else {
        return ("Student");
    }
}

function Details({ match }) {
    const { path } = match;
    const [profile, setProfile] = useState({});
    const user = accountService.userValue;
    React.useEffect(() => {
        accountService.getUserProfile()
        .then((res) => {
            setProfile(res.data)
        })
        .catch(err => console.log(err + " " + err.response))
      }, {});
   
    return (
        <div>
            <h1>My Profile</h1>
            <p>
                <strong>Name: </strong> {profile.first_name} {profile.last_name}<br />
                <strong>Email: </strong> {profile.email} <br />
                <strong>ID: </strong> {profile.id} <br/>
                <strong>Account Type: </strong> {facultyCheck(user.data.is_staff)}
            </p>
            <p><Link to={`${path}/update`}>Update Profile</Link></p>
            {/* <Tag/> */}
        </div>
    );
}

export { Details };
