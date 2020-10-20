import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './partial-component/header/header.component';
import { ContentComponent } from './partial-component/content/content.component';
import { RenameComponent } from './partial-component/rename/rename.component';
import { DeleteComponent } from './partial-component/delete/delete.component';
import { SpinnerComponent } from './partial-component/spinner/spinner.component';
import { AlertComponent } from './partial-component/alert/alert.component';
import { PreviewComponent } from './partial-component/preview/preview.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ContentComponent,
    RenameComponent,
    DeleteComponent,
    SpinnerComponent,
    AlertComponent,
    PreviewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
