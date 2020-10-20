import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class RestAPIService {

  constructor(
    private http: HttpClient) { }
  
  private URL= 'http://127.0.0.1:8000/upload'
  
  getData(filename:string, filetype:string, uploaddate:string): Observable<any> {
    let params = new HttpParams().set('filename',filename).set('filetype', filetype).set('uploaddate', uploaddate)
    return this.http.get(this.URL +'/database', {params: params})
  }
  uploadData(selectFile: File): Observable<any> {
    let formData: FormData = new FormData();
    formData.append('file', selectFile, selectFile.name);
    return this.http.post(this.URL, formData)
  }
  renameData(fileID:number, oldName:string, newName: string): Observable<any> {
    return this.http.put(this.URL, {id: fileID, old_filename: oldName, new_filename: newName})
  }
  deleteData(fileID:number, filePath:string, fileThumbnailPath:string): Observable<any> {
    let params = new HttpParams().set('id',fileID.toString()).set('file_path', filePath).set('file_thumbnail_path', fileThumbnailPath)
    return this.http.delete(this.URL, {params: params})
  }
}
