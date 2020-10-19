import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  constructor() { }

  private renameStatus = new BehaviorSubject({
    status: false,
    fileURL: '',
    fileID: 0,
    fileOldname: '',
    fileNewname: '',
    fileType: ''
  });
  currentRenameStatus = this.renameStatus.asObservable();

  openRename(status: boolean, fileURL:string, fileID: number, fileOldname: string, fileNewname: string, fileType: string) {
    this.renameStatus.next({status: status, fileURL: fileURL, fileID: fileID, fileOldname: fileOldname, fileNewname: fileNewname, fileType: fileType})
  }
}
