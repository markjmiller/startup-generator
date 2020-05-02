import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { MatExpansionPanel } from '@angular/material/expansion';
import { timer } from 'rxjs';

@Component({
  selector: 'app-disclaimer',
  templateUrl: './disclaimer.component.html',
  styleUrls: ['./disclaimer.component.css']
})
export class DisclaimerComponent implements OnInit, AfterViewInit {

  private displayFor = 5000;

  display = true;

  @ViewChild(MatExpansionPanel) panel: MatExpansionPanel;

  constructor() { }

  ngAfterViewInit(): void {
    timer(this.displayFor).subscribe(_ => this.panel.expanded = false);
  }

  ngOnInit(): void {
  }

  openTab(url: string){
    window.open(url, "_blank");
  }

  close(): void {
    this.display = false;
  }
}
