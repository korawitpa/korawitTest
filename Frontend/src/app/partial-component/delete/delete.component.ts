import { Component, OnInit } from '@angular/core';
import { PopupService } from '../../service/popup.service'
import { RestAPIService } from '../../service/rest-api.service'

@Component({
  selector: 'app-delete',
  templateUrl: './delete.component.html',
  styleUrls: ['./delete.component.css']
})
export class DeleteComponent implements OnInit {
  data = {}

  constructor(
    private popup_service: PopupService,
    private apiservice: RestAPIService) {
      this.popup_service.currentDeleteStatus.subscribe(
        result =>{
          this.data = result
        }
      )
     }

  ngOnInit(): void {
  }

  onCancel = () => {
    this.popup_service.openDelete(false, 0 , '', '', '')
  }

  onOK =() => {
    this.popup_service.openLoading(true)
    this.apiservice.deleteData(this.data['id'], this.data['file_path'], this.data['file_thumbnail_path']).subscribe(
      result => {
        this.popup_service.openLoading(false)
        this.popup_service.openAlert(true,'correct',result['msg'])
        this.onCancel()
      },
      error => {
        this.popup_service.openLoading(false)
        this.popup_service.openAlert(true,'alert',error.error['error'])
      }
    )
  }

}
