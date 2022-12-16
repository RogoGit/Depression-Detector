import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpResponse} from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Router } from '@angular/router';
import { User } from '../_models/User'

@Injectable()
export class AuthenticationService {
  constructor(private http: HttpClient, private router: Router) { }

  login(user: User) {
    console.log('Logged in with '+user);
    localStorage.setItem('currentUser', JSON.stringify(user) );
    // let headers = new HttpHeaders({
    // 'Content-Type': 'application/x-www-form-urlencoded'});
    // let options = { headers: headers };

    // var body = 'login=' + username + '&password=' + password;

    // return this.http.post<any>(`http://localhost:8080/MultHubnew_war_exploded/resources/user/signIn`, body/*{ username: username, password: password }*/, options)
    //   .pipe(map(user => {
    //     console.log(user);
    //     if (user && user.login) {
    //       localStorage.setItem('currentUser', JSON.stringify(user));
    //     }
    //     return user;
    //   }));
  }

  logout() {
    // remove user from local storage to log user out
    this.router.navigate(['login']);
    localStorage.removeItem('currentUser');    
    console.log('Logged out');
  }
}
