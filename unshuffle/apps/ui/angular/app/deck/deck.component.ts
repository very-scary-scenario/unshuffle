import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-deck',
  templateUrl: './deck.component.html',
})
export class DeckComponent implements OnInit {
  card = "Mario";

  constructor() { }

  ngOnInit() {
  }
}
