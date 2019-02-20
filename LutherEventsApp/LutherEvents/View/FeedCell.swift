//
//  FeedCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/23/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit
import Foundation
import SQLite

class FeedCell: BaseCell, UICollectionViewDataSource, UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    
    let cellId = "cellId"
    
    var events: [Event] = []
    //var events: AnySequence<Row>?

    func fetchEvents() {
        self.events = {
            let basketballPicture = Event()
            basketballPicture.title = "Women's Basketball - 7:00pm"
            basketballPicture.thumbnailImageName = "basketball2"
            basketballPicture.date = "1/14"
            basketballPicture.info = "Home vs Wartburg"

            let concertPicture = Event()
            concertPicture.title = "Quinn XCII Coming to Luther College - 9:00pm"
            concertPicture.thumbnailImageName = "Quinn_XCII"
            concertPicture.date = "2/22"
            concertPicture.info = "Located in Regents Center. Doors open @ 8:00pm. All are welcome!"

            let basketballPicture2 = Event()
            basketballPicture2.title = "Men's Basketball - 7:00pm"
            basketballPicture2.thumbnailImageName = "basketball2"
            basketballPicture2.date = "1/14"
            basketballPicture2.info = "Home vs Wartburg"

            let artPicture = Event()
            artPicture.title = "Student Art Show - 3:00pm-5:00pm"
            artPicture.thumbnailImageName = "ArtShow"
            artPicture.date = "2/06"
            artPicture.info = "Located in CFA. All are welcome!"

            let speakerPicture = Event()
            speakerPicture.title = "Obama's Coming to Luther Collge"
            speakerPicture.thumbnailImageName = "guestSpeaker"
            speakerPicture.date = "2/22"
            speakerPicture.info = "Located in CFL. Doors open @ 8:00pm. Tickets $10. More infomation on the website."

            return [basketballPicture, concertPicture, basketballPicture2, artPicture, speakerPicture]
        }()
    }
    
//    struct Events {
//        let id: Int
//        let eventName: String
//        let thumbnailImageName: String
//        let info: String
//        let category : String
//    }

    
    
    
    // makes accessible to all
    var database: Connection!

    // create table
    let eventsTable = Table("events")

    // create columns
    let id = Expression<Int>("id")
    let title = Expression<String>("eventName")
    let thumbnailImageName = Expression<String>("thumbnailImageName")
    let date = Expression<String>("date")
    let info = Expression<String>("info")
    let category = Expression<String>("category")
    
    func createAndMaintainDatabase() {
        //SETTING UP DATABASE, using SQLite
        // Creating a file to store data on users phone
        // File called events.sqlite3
        do {
            let documentDirectory = try FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
            let fileUrl = documentDirectory.appendingPathComponent("events").appendingPathExtension("sqlite3")
            let database = try Connection(fileUrl.path)
            self.database = database
            
        } catch {
            print("error1")
            print(error)
        }
        
        //DROPPING TABLE
//        do {
//            try self.database.run(self.eventsTable.drop(ifExists: true))
//            print("Table Dropped")
//        } catch {
//            print(error)
//        }

        //CREATING TABLE
//        let createTable = self.eventsTable.create { (table) in
//            table.column(self.id, primaryKey: true)
//            table.column(self.title)
//            table.column(self.thumbnailImageName)
//            table.column(self.date)
//            table.column(self.info)
//            table.column(self.category)
//        }
//
//        do {
//            try self.database.run(createTable)
//            print("Created Table")
//        } catch {
//            print("error2")
//        }
        
        //INSERTING DATA INTO TABLE
//        let insertEvent = self.eventsTable.insert(self.title <- "Women's Basketball - 7:00pm", self.thumbnailImageName <- "basketball2", self.date <- "2/03", self.info <- "Home vs Wartburg", self.category <- "Athletics")
//
//        let insertEvent1 = self.eventsTable.insert(self.title <- "Quinn XCII Coming to Luther College - 9:00pm", self.thumbnailImageName <- "concertPicture", self.date <- "2/22", self.info <- "Located in Regents Center. Doors open @ 8:00pm. All are welcome!", self.category <- "Arts")
//
//        let insertEvent2 = self.eventsTable.insert(self.title <- "Obama's Coming to Luther Collge", self.thumbnailImageName <- "speakerPicture", self.date <- "3/15", self.info <- "Located in CFL. Doors open @ 8:00pm. Tickets $10. More infomation on the website.", self.category <- "Other")
//
//
//        do {
//            try self.database.run(insertEvent)
//            try self.database.run(insertEvent1)
//            try self.database.run(insertEvent2)
//            print("INSERTED EVENT")
//        } catch {
//            print("error3")
//            print(error)
//        }
//
        //        // UPDATING EVENT
        //        let eventToUpdate = 1
        //        let event = self.eventsTable.filter(self.id == eventToUpdate)
        //        let updateEvent = event.update(self.eventName <- "Men's Basketball - 8:30pm")
        //        do {
        //            try self.database.run(updateEvent)
        //        } catch {
        //            print("error5")
        //            print(error)
        //        }
        //
        //        // DELETING EVENT
        //        let eventToDelete = 1
        //        let eventD = self.eventsTable.filter(self.id == eventToDelete)
        //        let deleteEvent = eventD.delete()
        //        do {
        //            try self.database.run(deleteEvent)
        //        } catch {
        //            print("error6")
        //            print(error)
        //        }
        
        // SHOW EVENETS
        do {
            let events = try self.database.prepare(self.eventsTable)
            for event in events {
                print("id: \(event[self.id]), title: \(event[self.title]), thumbnailImageName: \(event[self.thumbnailImageName]), date: \(event[self.date]), info: \(event[self.info])")
                //print(event)
            }
        } catch  {
            print("error4")
            print(error)
        }
    }
    
    
//    func fetchEvents() -> AnySequence<Row>? {
//        do {
//            return try self.database.prepare(self.eventsTable)
//        } catch {
//            print("could not fetch events")
//            print(error)
//            return nil
//        }
//    }

    // create a collection view
    // use lazy var to access self within closed block
    lazy var collectionView: UICollectionView = {
        let layout = UICollectionViewFlowLayout()
        let cv = UICollectionView(frame: .zero, collectionViewLayout: layout)
        cv.backgroundColor = UIColor.white
        cv.dataSource = self
        cv.delegate = self
        return cv
    }()
    
    override func setupViews() {
        super.setupViews()
        
        createAndMaintainDatabase()
        
//        if let eventsTable: AnySequence<Row> = queryAll() {
//
//        }
        
        fetchEvents()

    
        addSubview(collectionView)
        addConstraintsWithFormat(format: "H:|[v0]|", views: collectionView)
        addConstraintsWithFormat(format: "V:|[v0]|", views: collectionView)
        
        collectionView.register(PictureCell.self, forCellWithReuseIdentifier: cellId)
    }
    
    // Make the Status Bar Light Content for every View (gets called by line above, setNeedsStatusBarAppearanceUpdate)
    var preferredStatusBarStyle: UIStatusBarStyle {
        return .lightContent
    }
    
    // creating the cells
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        
//        var numOfEvents: Int = 0
//        for _ in events! {
//            //print("id: \(event[self.id]), eventName: \(event[self.eventName]), thumbnailImageName: \(event[self.thumbnailImageName]), date: \(event[self.date]), info: \(event[self.info])")
//            numOfEvents += 1
//        }
//        return numOfEvents

        return events.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell
    {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cellId", for: indexPath) as! PictureCell
        
//        for ev in events! {
//            print(ev)
//            if indexPath.item == (ev[self.id] - 1) {
//                //cell.event = ev
//                return cell
//            }
//        }
//
//        print(events)
        cell.event = events[indexPath.item]
        return cell
    }
    
    //Sets each cell to the width of the frame and height of 200
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let height = (frame.width - 16 - 16) * 9 / 16
        return CGSize(width: (frame.width), height: height + 16 + 88)
    }
    
    //Gets rid of the extra padding/margin space inbetween the cells
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }
    
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let eventLauncher = EventLauncher()
        eventLauncher.showEvent()
//        for ev in events! {
//            if (ev[self.id] - 1) == indexPath.item {
//                showEvent()
//
//            }
//        }
        //_ = events[indexPath.item]
        //print(event.thumbnailImageName!)
        //showEvent()
    }
    
    let view = UIView()
    
    func showEvent() {
        //print("event here")
        
        // because its an nsobject there is no access to the window view so key window lets us access the frame
        if let keyWindow = UIApplication.shared.keyWindow {
            
            //let view = UIView(frame: keyWindow.frame)
            
            // background view
            view.backgroundColor = UIColor.black
            //view.frame = CGRect(x: keyWindow.frame.width - 10, y: keyWindow.frame.height - 10, width: 10, height: 10)
            
            view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(handleExit)))
            
            keyWindow.addSubview(view)
            view.frame = keyWindow.frame
            
            // picture view
            // 16 x 9 is the aspect ratio to all HD videos
            let height = keyWindow.frame.height - 200
            let pictureFrame = CGRect(x: 0, y: 0, width: keyWindow.frame.width, height: height)
            
            let  pictureView = PictureView(frame: pictureFrame)
            view.addSubview(pictureView)
            
            // creates animation from bottom right to fill the whole screen
            UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 1, initialSpringVelocity: 1, options: .curveEaseOut, animations: {
            }, completion: {(completedAnimation) in
                self.view.alpha = 1
                self.createContent()
            })
        }
    }
    
    func createContent() {
        

    }
    
    @objc func handleExit() {
        UIView.animate(withDuration: 0.5) {
            self.view.alpha = 0
        }
    }
    
    class PictureView: UIView {
        override init(frame: CGRect) {
            super.init(frame: frame)

            //let event = events[IndexPath]
            //event.thumbnailImageView
            
            let image = UIImage(named: "LutherCollegeLogo")
            let imageView = UIImageView(image: image!)
            imageView.contentMode = .scaleAspectFill
            imageView.clipsToBounds = true
            
            let gradient: CAGradientLayer = CAGradientLayer()
            gradient.frame = imageView.frame
            gradient.colors = [UIColor.clear.cgColor, UIColor.black.cgColor]
            gradient.locations = [0.0, 0.41]
            imageView.layer.insertSublayer(gradient, at: 0)
            
            imageView.frame = CGRect(x: 0, y: 0, width: frame.width, height: 400)
            self.addSubview(imageView)
        }
        
        required init?(coder aDecoder: NSCoder) {
            fatalError("init(coder:) has not been implemented")
        }
    }
}


