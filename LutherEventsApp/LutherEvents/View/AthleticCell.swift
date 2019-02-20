//
//  AthleticCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/23/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

class AthleticCell: FeedCell {
    
//    override func fetchEvents() -> AnySequence<Row>? {
//        do {
//            return try self.database.prepare(self.eventsTable)
//        } catch {
//            print("could not fetch events")
//            print(error)
//            return nil
//        }
//    }

    
    override func fetchEvents() {
        self.events = {
            let basketballPicture2 = Event()
            basketballPicture2.title = "Men's Basketball - 7:00pm"
            basketballPicture2.thumbnailImageName = "basketball2"
            basketballPicture2.date = "1/14"
            basketballPicture2.info = "Home vs Wartburg"

            return [basketballPicture2]
        }()
    }
}
