//
//  ArtCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/23/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

class ArtCell: FeedCell {
    
    override func fetchEvents() {
        self.events = {
            let artPicture = Event()
            artPicture.title = "Student Art Show - 3:00pm-5:00pm"
            artPicture.thumbnailImageName = "ArtShow"
            artPicture.date = "2/06"
            artPicture.info = "Located in CFA. All are welcome!"
            
            return [artPicture]
        }()
    }
}
