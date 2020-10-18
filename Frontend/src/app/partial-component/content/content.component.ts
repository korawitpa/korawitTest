import { Component, OnInit } from '@angular/core';
import { RestAPIService } from '../../service/rest-api.service'

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {

  constructor(private apiservice: RestAPIService) { }

  ngOnInit(): void {
    this.getdatabase()
  }
  images: []
  getdatabase() {
    this.apiservice.getData().subscribe(
      result => {
        result['msg'].forEach(element => {
          element['URL'] = 'http://127.0.0.1:8000/upload/' + element['FileName'] + '/thumbnail'
          console.log(element['URL'])
        });
        this.images = result['msg']
        console.log(this.images)
      },
      error => {
        console.log(error)
      }
    )
  }
  upload(event){
    if (event.target.files.length > 0){
      this.apiservice.uploadData(event.target.files[0]).subscribe(
        result => {
          console.log(result)
        },
        error => {
          console.log(error)
        }
      )
    }
  }
}
