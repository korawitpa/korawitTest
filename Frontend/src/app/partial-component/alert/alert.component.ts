import { Component, OnInit } from '@angular/core';
import { PopupService } from '../../service/popup.service'

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.css']
})
export class AlertComponent implements OnInit {

  data = {}

  constructor(
    private popup_service: PopupService
  ) {
    this.popup_service.currentAlertStatus.subscribe(
      result => {
        this.data = result
      }
    )
   }

  ngOnInit(): void {
  }

  onOK() {
    this.popup_service.openAlert(false,'','')
    location.reload()
  }
}
