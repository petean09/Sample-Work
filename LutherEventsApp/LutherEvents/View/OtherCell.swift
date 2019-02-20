//
//  OtherCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/23/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

class OtherCell: FeedCell {
    
    override func fetchEvents() {
        self.events = {
            let speakerPicture = Event()
            speakerPicture.title = "Obama's Coming to Luther Collge"
            speakerPicture.thumbnailImageName = "guestSpeaker"
            speakerPicture.date = "2/22"
            speakerPicture.info = "Located in CFL. Doors open @ 8:00pm. Tickets $10. More infomation on the website."
            
            return [speakerPicture]
        }()
    }
}
