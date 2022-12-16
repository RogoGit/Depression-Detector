import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

@Injectable()
export class ManagerGuard implements CanActivate {

  constructor(private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
      console.log("GUARD");
    // localStorage.setItem('currentUser', 'divand');
    if (localStorage.getItem('currentUser')) {
      // logged in so return true
      // localStorage.clear();
      return true;
    }

    // not logged in so redirect to login page with the return url
    alert('U have to log in first');
    this.router.navigate(['login']
      //, { queryParams: { returnUrl: state.url }}
    );
    return false;
  }
}
