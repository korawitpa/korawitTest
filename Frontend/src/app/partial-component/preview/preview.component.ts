import { Component, OnInit } from '@angular/core';
import { PopupService } from '../../service/popup.service'

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.css']
})
export class PreviewComponent implements OnInit {
  data = {}

  constructor(
    private popup_service: PopupService
  ) { 
    this.popup_service.currentPreviewStatus.subscribe(
      result => {
        this.data = result
        if (result['type'] != ''){
          if (result['type'].split('/')[0] === 'image'){
            this.data['type'] = 'image'
          }
          else{
            this.data['type'] = 'video'
          }
        }
      }
    )
  }

  ngOnInit(): void {
  }

  onClose(){
    if (this.data['type'] == 'video'){
      let myVideo: any = document.getElementById("myVideo")
      myVideo.pause()
    } 
    this.popup_service.openPreview(false, '' ,'')
  }

}
