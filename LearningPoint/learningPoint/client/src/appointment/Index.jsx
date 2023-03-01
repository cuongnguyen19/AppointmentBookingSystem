import React from 'react';
import { Route, Switch } from 'react-router-dom';

import DataTable from './Table';
import MyTable from './MyTable';
import { accountService } from '@/_services';
import { useLocation } from "react-router-dom";


function Appointment({ match }) {
    const { path } = match;
    const user = accountService.userValue;
    
    return (
        <div className="p-4">
            <div className="container">
                <Switch>
                {user.data.is_staff == true? 
                (<Route exact path={path} component={DataTable} />) :
                (<Route exact path={path} component={MyTable} />)}
                </Switch>
            </div>
        </div>
    );
}

export { Appointment };