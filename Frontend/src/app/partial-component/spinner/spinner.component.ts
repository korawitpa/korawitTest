import { Component, OnInit } from '@angular/core';
import { PopupService } from '../../service/popup.service'

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.css']
})
export class SpinnerComponent implements OnInit {
  status = false

  constructor(
    private popup_service: PopupService
  ) { 
    this.popup_service.currentLoadingStatus.subscribe(
      result => {
        this.status =  result
      }
    )
  }

  ngOnInit(): void {
  }
  
}
