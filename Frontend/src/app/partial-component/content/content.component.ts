import { Component, OnInit } from '@angular/core';
import { RestAPIService } from '../../service/rest-api.service'
import { PopupService } from '../../service/popup.service'

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {

  constructor(
    private apiservice: RestAPIService,
    private popup_service: PopupService) { }

  ngOnInit(): void {
    this.getdatabase()
  }

  images: []
  filter: {} = {
    filename: '',
    filetype: '',
    uploaddate: ''
  }

  getdatabase() {
    this.popup_service.openLoading(true)
    if (this.filter['filetype'] != ''){
      if (this.filter['filetype'] == 'mp4'){
        this.filter['filetype'] = 'video/' + this.filter['filetype']
      }
      else {
        this.filter['filetype'] = 'image/' + this.filter['filetype']
      }
    }
    this.apiservice.getData(this.filter['filename'], this.filter['filetype'], this.filter['uploaddate']).subscribe(
      result => {
        this.popup_service.openLoading(false)
        result['msg'].forEach(element => {
          element['URL'] = 'http://127.0.0.1:8000/upload/' + element['FileName'] + '/thumbnail'
        });
        this.images = result['msg']
      },
      error => {
        this.popup_service.openLoading(false)
        if (error.status == 0){
          this.popup_service.openAlert(true, 'alert', "Can't connect API please check")
        }
        else{
          this.popup_service.openAlert(true, 'alert', error.error['error'])
        }
      }
    )
  }
  upload(event){
    this.popup_service.openLoading(true)
    if (event.target.files.length > 0){
      this.apiservice.uploadData(event.target.files[0]).subscribe(
        result => {
          this.popup_service.openLoading(false)
          this.getdatabase()
          // this.popup_service.openAlert(true, 'correct', result['msg'])
        },
        error => {
          this.popup_service.openLoading(false)
          console.log(error)
          if (error.status == 406){
            this.popup_service.openAlert(true, 'alert', error.error['error'])
          }
          else{
            this.popup_service.openAlert(true, 'alert', 'Check your file do not excess 50MB')
          }
          
        }
      )
    }
  }
  onRename(file){
    this.popup_service.openRename(true, file['URL'].replace('/thumbnail', ''), file['ID'], file['FilePath'], '', file['FileType'])
  }
  onDelete(file){
    this.popup_service.openDelete(true, file['ID'], file['FileName'], file['FilePath'], file['FileThumbnailPath'])
  }
  onPreview(file){
    this.popup_service.openPreview(true, file['FileType'], file['URL'].replace('/thumbnail', ''))
  }
}
