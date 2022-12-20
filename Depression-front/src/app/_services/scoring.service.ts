import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpResponse} from '@angular/common/http';


@Injectable()
export class ScoringService {
  constructor(private http: HttpClient) { }

  score(event: any){
    return this.http.post("http://dumbass.sytes.net:55557/models/",event);
  }



}
