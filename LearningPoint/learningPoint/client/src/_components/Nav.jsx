import React, { useState, useEffect } from 'react';
import { NavLink, Route } from 'react-router-dom';

import { Role } from '@/_helpers';
import { accountService } from '@/_services';

function checkStudent(checking){
    if(checking){

    }
   else{
    return  (<NavLink to="/profile" className="nav-item nav-link">Booked Appointment</NavLink>);
    }
}


function Nav() {
    const [user, setUser] = useState({});

    useEffect(() => {
        const subscription = accountService.user.subscribe(x => setUser(x));
        return subscription.unsubscribe;
    }, []);

    // only show nav when logged in
    if (!user) return null;

    return (
        <div>
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <div className="navbar-nav">
                    <NavLink exact to="/" className="nav-item nav-link">
                    <h5 className='icon-learning'>Learning</h5><h5 className='icon-point'>Point</h5>
                    </NavLink>
                    <NavLink to="/appointment" className="nav-item nav-link">Appointment</NavLink>
                    {/* {checkStudent(user.data.is_staff)}; */}


                    {/* {user.data ? user.data.is_staff == false?
                    (<NavLink to="/booked-appointment" className="nav-item nav-link">Booked Appointment</NavLink>) :
                    (<NavLink to="/profile" className="nav-item nav-link">Profile</NavLink>) : null } */}


                    <NavLink to="/profile" className="nav-item nav-link">Profile</NavLink>
                    {user.role === Role.Admin &&
                        <NavLink to="/admin" className="nav-item nav-link">Admin</NavLink>
                    }
                    <a onClick={accountService.logout} className="nav-item nav-link">Logout</a>
                </div>
            </nav>
            <Route path="/admin" component={AdminNav} />
        </div>
    );
}

function AdminNav({ match }) {
    const { path } = match;

    return (
        <nav className="admin-nav navbar navbar-expand navbar-light">
            <div className="navbar-nav">
                <NavLink to={`${path}/users`} className="nav-item nav-link">Users</NavLink>
            </div>
        </nav>
    );
}

export { Nav };