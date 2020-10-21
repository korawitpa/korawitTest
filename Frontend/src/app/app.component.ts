import { Component } from '@angular/core';
import { from } from 'rxjs';
import { RestAPIService } from './service/rest-api.service'
import { PopupService } from './service/popup.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular';
  image: any

  constructor(
    private restapi: RestAPIService,
    private popup_service: PopupService) { }
  
  ngOnInit() {
    // this.getData();
  }

  // getData = () => {
  //   this.popup_service.openLoading(true)
  //   this.restapi.getData().subscribe(
  //     result => {
  //       this.popup_service.openLoading(false)
  //       this.image = result
  //     },
  //     error => {
  //       this.popup_service.openLoading(false)
  //       console.log(error.error)
  //     })
  // }

}
