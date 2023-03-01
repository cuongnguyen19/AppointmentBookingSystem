import React from 'react';

import { accountService } from '@/_services';

function Home() {
    const user = accountService.userValue;
    
    return (
        <div className="p-4">
            <div className="container">
                <h1>Hi {user.data.first_name}!</h1>
                <p>Welcome to appointment booking system. Please choose a desire operation on the top bar</p>
            </div>
        </div>
    );
}

export { Home };