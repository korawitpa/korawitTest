import { Component, Input, OnInit } from '@angular/core';
import { error } from 'protractor';
import { PopupService } from '../../service/popup.service'
import { RestAPIService } from '../../service/rest-api.service'

@Component({
  selector: 'app-rename',
  templateUrl: './rename.component.html',
  styleUrls: ['./rename.component.css']
})
export class RenameComponent implements OnInit {

  data: {}
  newFilename: string

  constructor(
    private popup_service: PopupService,
    private apiservice: RestAPIService
    ) {
    this.popup_service.currentRenameStatus.subscribe(
      result => {
        this.newFilename = ''  // Clear new filename
        this.data = result
        if (result['fileType'] != ''){
          this.data['onlyOldFilename'] = this.data['fileOldname'].split('\\')[1].split('.')[0]
          this.data['directory'] = this.data['fileOldname'].split('\\')[0]
          this.data['typeofFile'] = this.data['fileOldname'].split('\\')[1].split('.')[1]
          if (result['fileType'].split('/')[0] === 'image'){
            this.data['fileType'] = 'image'
          }
          else{
            this.data['fileType'] = 'video'
          }
        }
      }
    )
  }

  ngOnInit(): void {
  }

  onCancel = () => {
    this.popup_service.openRename(false, '', 0 ,'' ,'', '')
  }

  onOK =() => {
    this.popup_service.openLoading(true)
    this.data['fileNewname'] = this.data['directory'] + '/' + this.newFilename + '.' + this.data['typeofFile']
    this.data['fileOldname'] = this.data['fileOldname'].replace('\\','/')
    this.apiservice.renameData(this.data['fileID'], this.data['fileOldname'], this.data['fileNewname']).subscribe(
      result => {
        this.onCancel()
        this.popup_service.openLoading(false)
        this.popup_service.openAlert(true,'correct',result['msg'])
      },
      error => {
        this.popup_service.openLoading(false)
        this.popup_service.openAlert(true,'alert',error.error['error'])
      }
    )
  }

}
