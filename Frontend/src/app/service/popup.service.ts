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

  private deleteStatus = new BehaviorSubject({
    status: false,
    id: 0,
    file_name: '',
    file_path: '',
    file_thumbnail_path: ''
  });
  currentDeleteStatus = this.deleteStatus.asObservable();

  openDelete(status: boolean, fileID: number, fileName: string, filePath: string, fileThumbnailPath: string) {
    this.deleteStatus.next({status: status, id: fileID, file_name: fileName, file_path: filePath, file_thumbnail_path: fileThumbnailPath})
  }

  private loadingStatus = new BehaviorSubject(false);
  currentLoadingStatus = this.loadingStatus.asObservable();

  openLoading(status: boolean) {
    this.loadingStatus.next(status)
  }

  private alertStatus = new BehaviorSubject(
    {
      status: false,
      type: '',
      message: ''
    }
  );
  currentAlertStatus = this.alertStatus.asObservable();

  openAlert(status: boolean, type: string, message: string) {
    this.alertStatus.next({status:status, type:type, message:message})
  }

  private previewStatus = new BehaviorSubject(
    {
      status: false,
      type: '',
      url: ''
    }
  );
  currentPreviewStatus = this.previewStatus.asObservable();

  openPreview(status: boolean, type: string, url: string) {
    this.previewStatus.next({status:status, type:type, url:url})
  }
}
