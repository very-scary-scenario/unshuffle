import { Component, OnInit } from '@angular/core';
import { Card } from '../card';
import { CARDS } from '../mock-cards';

@Component({
  selector: 'app-deck',
  templateUrl: './deck.component.html',
})
export class DeckComponent implements OnInit {
  cards = CARDS;

  constructor() { }

  ngOnInit() {
  }
}
