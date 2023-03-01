import { BehaviorSubject } from 'rxjs';
import {Buffer} from 'buffer';

import config from 'config';
import { fetchWrapper, history } from '@/_helpers';
import http from "./http-common";

const userSubject = new BehaviorSubject(null);
const baseUrl = `${config.apiUrl}/accounts`;

export const accountService = {
    login,
    logout,
    refreshToken,
    register,
    createAppointment,
    getAllAppointments,
    getBookedAppointments,
    bookAppointment,
    unbookAppointment,
    updateAppointment,
    deleteAppointment,
    verifyEmail,
    forgotPassword,
    changePassword,
    getUserProfile,
    validateResetToken,
    resetPassword,
    getAll,
    getById,
    create,
    update,
    delete: _delete,
    user: userSubject.asObservable(),
    get userValue () { return userSubject.value }
};

function login(data) {
    return http.post("/login", data)
        .then(user => {
            // publish user to subscribers and start timer to refresh token
            userSubject.next(user);
            //startRefreshTokenTimer1();
            return user;
        });
}

function logout() {
    // revoke token, stop refresh timer, publish null to user subscribers and redirect to login page
    localStorage.clear();
    userSubject.next(null);
    history.push('/account/login');
}

function refreshToken() {
    return fetchWrapper.post(`${baseUrl}/refresh-token`, {})
        .then(user => {
            // publish user to subscribers and start timer to refresh token
            userSubject.next(user);
            startRefreshTokenTimer();
            return user;
        });
}

function register(data) {
    return http.post("/register", data);
}

function createAppointment(data) {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.post("/create-appointment", data, {
        headers: {
            'Authorization': 'Basic ' + encodedToken
          }
    })
}

function getAllAppointments() {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.get("/view-appointment-list", {
        headers: {
            'Authorization': 'Basic ' + encodedToken
          }
    })
}

function getBookedAppointments() {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.get("/view-booked-appointment-list", {
        headers: {
            'Authorization': 'Basic ' + encodedToken
          }
    })
}

function bookAppointment(id) {
    var data = {};
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.put("/book-appointment/" + id, data, {
      headers: {
        'Authorization': 'Basic ' + encodedToken
      }
    })
}

function unbookAppointment(id) {
    var data = {};
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.put("/unbook-appointment/" + id, data, {
      headers: {
        'Authorization': 'Basic ' + encodedToken
      }
    })
}

function updateAppointment(data) {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.put("/update-appointment/" + data.id, data, {
      headers: {
        'Authorization': 'Basic ' + encodedToken
      }
    })
}

function deleteAppointment(id) {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');

    return http.delete("/delete-appointment/" + id, {
      headers: {
        'Authorization': 'Basic ' + encodedToken
      }
    })
}

function verifyEmail(token) {
    return fetchWrapper.post(`${baseUrl}/verify-email`, { token });
}

function forgotPassword(email) {
    return http.post("/reset-password", email);
}

function changePassword(data) {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');

    return http.put("/change-password", data, {
        headers: {
          'Authorization': 'Basic ' + encodedToken
        }
      });
}

function getUserProfile() {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.get("/profile", {
        headers: {
            'Authorization': 'Basic ' + encodedToken
          }
    })
}

function validateResetToken(token) {
    return fetchWrapper.post(`${baseUrl}/validate-reset-token`, { token });
}

function resetPassword({ token, password, confirmPassword }) {
    return fetchWrapper.post(`${baseUrl}/reset-password`, { token, password, confirmPassword });
}

function getAll() {
    return fetchWrapper.get(baseUrl);
}

function getById(id) {
    return fetchWrapper.get(`${baseUrl}/${id}`);
}

function create(params) {
    return fetchWrapper.post(baseUrl, params);
}

function update(id, params) {
    var username = localStorage.getItem('username');
    var password= localStorage.getItem('password');
    const token = `${username}:${password}`;
    const encodedToken = Buffer.from(token).toString('base64');
    return http.put("/update-profile/" + id, params, {
        headers: {
          'Authorization': 'Basic ' + encodedToken
        }
    })
}

// prefixed with underscore because 'delete' is a reserved word in javascript
function _delete(id) {
    return fetchWrapper.delete(`${baseUrl}/${id}`)
        .then(x => {
            // auto logout if the logged in user deleted their own record
            if (id === userSubject.value.id) {
                logout();
            }
            return x;
        });
}

// helper functions

let refreshTokenTimeout;

function startRefreshTokenTimer() {
    // parse json object from base64 encoded jwt token
    const jwtToken = JSON.parse(atob(userSubject.value.token.split('.')[1]));

    // set a timeout to refresh the token a minute before it expires
    const expires = new Date(jwtToken.exp * 1000);
    const timeout = expires.getTime() - Date.now() - (60 * 1000);
    refreshTokenTimeout = setTimeout(refreshToken, timeout);
}
