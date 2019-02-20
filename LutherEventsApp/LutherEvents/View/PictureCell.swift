//
//  PictureCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/14/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

// BaseCell is created so initial setup of cells does not have to be done everytime. This is a super class of PictureCell and MenuCell
class BaseCell: UICollectionViewCell {
    override init(frame: CGRect) {
        super.init(frame: frame)
        setupViews()
    }
    
    func setupViews() {

    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

//create the custom cells
class PictureCell: BaseCell {
    
    // this modifies the heights of the titles so the titles can be one or two lines depending on the length of words
    var titleLabelHeightConstraint: NSLayoutConstraint?
    
    //creating an event cell so the HomeController can use it
    var event: Event? {
        didSet {
            titleLabel.text = event?.title
            thumbnailImageView.image = UIImage(named: (event?.thumbnailImageName)!)
            dateLabel.text = event?.date
            subtitleTextView.text = event?.info
            
            //measure the title text
            if let title = event?.title {
                let size = CGSize(width: frame.width - 16 - 44 - 8 - 16, height: 1000)
                let estimatedRect = NSString(string: title).boundingRect(with: size, options: NSStringDrawingOptions.usesFontLeading.union(.usesLineFragmentOrigin), attributes: [NSAttributedString.Key.font: UIFont.systemFont(ofSize: 14)], context: nil)
                
                if estimatedRect.size.height > 20 {
                    titleLabelHeightConstraint?.constant = 44
                } else {
                    titleLabelHeightConstraint?.constant = 20
                }
            }
        }
    }

    // Makes the section for the picture
    let thumbnailImageView: UIImageView = {
        let imageView = UIImageView()
        //imageView.image = UIImage(named: "basketball2")
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        return imageView
    }()
    
    // Makes a line to seperate cells
    let separatorView: UIView = {
        let view = UIView()
        view.backgroundColor = UIColor.init(red: 230/255, green: 230/255, blue: 230/255, alpha: 1)
        return view
    }()
    
    // Makes the title section
    let titleLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        //label.text = "Women's Basketball - 7:00pm"
        label.numberOfLines = 2
        return label
    }()
    
    // Makes the date section
    let dateLabel: UILabel = {
        let dlabel = UILabel()
        dlabel.translatesAutoresizingMaskIntoConstraints = false
        //dlabel.text = "1/14"
        return dlabel
    }()
    
    // Makes the subtitle section
    let subtitleTextView: UITextView = {
        let textView = UITextView()
        textView.translatesAutoresizingMaskIntoConstraints = false
        //textView.text = "Home vs Wartburg"
        textView.textContainerInset = UIEdgeInsets(top: 0, left: -4, bottom: 0, right: 0)
        textView.textColor = UIColor.lightGray
        return textView
    }()
    
    // This function creates the elements and specifies where the elements will go
    override func setupViews() {
        //sets up basecell
        super.setupViews()
        
        // adds the picture spot
        addSubview(thumbnailImageView)
        // adds a cell separator
        addSubview(separatorView)
        // adds title label
        addSubview(titleLabel)
        // adds date label
        addSubview(dateLabel)
        // adds subtitle label
        addSubview(subtitleTextView)
        
        // CONSTRAINTS (the pipe specifies the edge of the cell)
        //space of 16 pixels from the right and left. Anything in the middle is filled with the image
        addConstraintsWithFormat(format: "H:|-16-[v0]-16-|", views: thumbnailImageView)
        //dateLabel constraints
        addConstraintsWithFormat(format: "H:|-16-[v0(44)]", views: dateLabel)
        
        //space of 16 pixels from the top and bottom. Anything in the middle is filled with the image. 8 pixels inbetween the labels. Then a pixel width separatorView is added to the bottom of each cell.
        addConstraintsWithFormat(format: "V:|-16-[v0]-8-[v1(44)]-36-[v2(1)]|", views: thumbnailImageView, dateLabel, separatorView)
        
        // the separatorView spans from left to right
        addConstraintsWithFormat(format: "H:|[v0]|", views: separatorView)
        
        //titleLabel (doing it this way is better because when the titleLabel gets bigger the subtitleTextView can adjust)
        //top constraint
        addConstraint(NSLayoutConstraint(item: titleLabel, attribute: .top, relatedBy: .equal, toItem: thumbnailImageView, attribute: .bottom, multiplier: 1, constant: 8))
        //left constraint
        addConstraint(NSLayoutConstraint(item: titleLabel, attribute: .left, relatedBy: .equal, toItem: dateLabel, attribute: .right, multiplier: 1, constant: 8))
        //right constraint
        addConstraint(NSLayoutConstraint(item: titleLabel, attribute: .right, relatedBy: .equal, toItem: thumbnailImageView, attribute: .right, multiplier: 1, constant: 0))
        //height constraint
        titleLabelHeightConstraint = NSLayoutConstraint(item: titleLabel, attribute: .height, relatedBy: .equal, toItem: self, attribute: .height, multiplier: 0, constant: 44)
        addConstraint(titleLabelHeightConstraint!)
        
        //subtitleTextView
        //top constraint
        addConstraint(NSLayoutConstraint(item: subtitleTextView, attribute: .top, relatedBy: .equal, toItem: titleLabel, attribute: .bottom, multiplier: 1, constant: 4))
        //left constraint
        addConstraint(NSLayoutConstraint(item: subtitleTextView, attribute: .left, relatedBy: .equal, toItem: dateLabel, attribute: .right, multiplier: 1, constant: 8))
        //right constraint
        addConstraint(NSLayoutConstraint(item: subtitleTextView, attribute: .right, relatedBy: .equal, toItem: thumbnailImageView, attribute: .right, multiplier: 1, constant: 0))
        //height constraint
        addConstraint(NSLayoutConstraint(item: subtitleTextView, attribute: .height, relatedBy: .equal, toItem: self, attribute: .height, multiplier: 0, constant: 30))
    }
}

