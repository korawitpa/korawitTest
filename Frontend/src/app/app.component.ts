import { Component } from '@angular/core';
import { from } from 'rxjs';
import { RestAPIService } from './service/rest-api.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular';
  image: any

  constructor(
    private restapi: RestAPIService) { }
  
  ngOnInit() {
    // this.getData();
  }

  getData = () => {
    this.restapi.getData().subscribe(
      result => {
        this.image = result
        console.log(this.image)
      },
      error => {
        console.log(error.error)
      })
  }

}
