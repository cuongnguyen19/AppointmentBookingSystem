import http from "./http-common";
import { BehaviorSubject } from 'rxjs';


const userSubject = new BehaviorSubject(null);


class UserDataService {
  register(data) {
    return http.post("/register", data);
  }
  login(data) {
    return http.post("/login", data)
        .then(user => {
          // publish user to subscribers 
        userSubject.next(user);
        return user;
        });
  }
  getAllAppointments() {
    return http.get("/view-appointment-list", {
      auth: {
        username: localStorage.getItem('username'),
        password: localStorage.getItem('password'),
      }
    }).then(response => {
      
      return response;
  });;
  }
  
}

export default new UserDataService();