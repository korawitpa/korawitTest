import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class RestAPIService {

  constructor(
    private http: HttpClient) { }
  
  private URL= 'http://127.0.0.1:8000/upload'
  
  getData(): Observable<any> {
    return this.http.get(this.URL +'/database')
  }
  uploadData(selectFile: File): Observable<any> {
    let formData: FormData = new FormData();
    formData.append('file', selectFile, selectFile.name);
    return this.http.post(this.URL, formData)
  }
}
