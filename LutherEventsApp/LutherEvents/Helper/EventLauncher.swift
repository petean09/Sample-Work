//
//  EventLauncher.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/24/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

class PictureView: UIView {
    override init(frame: CGRect) {
        super.init(frame: frame)

//        if let eventArray : Any = UserDefaults.standard.object(forKey: "eventKey") {
//            let readArray : [NSString] = eventArray as! [NSString]
//        }
//
//        let imageName = readArray.thumbnailImageView
        let image = UIImage(named: "basketball2")
        let imageView = UIImageView(image: image!)
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true

        let gradient: CAGradientLayer = CAGradientLayer()
        gradient.frame = imageView.frame
        gradient.colors = [UIColor.clear.cgColor, UIColor.black.cgColor]
        gradient.locations = [0.0, 0.8]
        imageView.layer.insertSublayer(gradient, at: 0)

        imageView.frame = CGRect(x: 0, y: 0, width: frame.width, height: 450)
        self.addSubview(imageView)

        //backgroundColor = UIColor.white

    }

    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

class EventLauncher: NSObject{

    func showEvent() {
        //print("event here")

        // because its an nsobject there is no access to the window view so key window lets us access the frame
        if let keyWindow = UIApplication.shared.keyWindow {
            let view = UIView(frame: keyWindow.frame)

            // background view
            view.backgroundColor = UIColor.black
            view.frame = CGRect(x: keyWindow.frame.width - 10, y: keyWindow.frame.height - 10, width: 10, height: 10)
            keyWindow.addSubview(view)

            // picture view
            // 16 x 9 is the aspect ratio to all HD videos
            let height = keyWindow.frame.height - 200
            let pictureFrame = CGRect(x: 0, y: 0, width: keyWindow.frame.width, height: height)
            let pictureView = PictureView(frame: pictureFrame)
            view.addSubview(pictureView)

            // creates animation from bottom right to fill the whole screen
            UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 1, initialSpringVelocity: 1, options: .curveEaseOut, animations: {
                view.frame = keyWindow.frame
            }, completion: {(completedAnimation) in
                    //do something here later
            })
        }
    }
}
////    func createContent() {
////        let feedCell = FeedCell()
////        feedCell.fetchEvents()
////    }
//}
