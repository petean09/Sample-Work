//
//  SettingCell.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/21/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

// creates the infomation that goes inside the cells of the collectionView(settings menu)
class SettingCell: BaseCell {
    
    //when cell button is highlighted the properties change
    override var isHighlighted: Bool {
        didSet {
            backgroundColor = isHighlighted ? UIColor.darkGray : UIColor.white
            nameLabel.textColor = isHighlighted ? UIColor.white : UIColor.black
            iconImageView.tintColor = isHighlighted ? UIColor.white : UIColor.darkGray
        }
    }
    
    var setting: Setting? {
        didSet {
            nameLabel.text = (setting?.name).map { $0.rawValue }
            
            if let imageName = setting?.imageName {
                iconImageView.image = UIImage(named: imageName)?.withRenderingMode(.alwaysTemplate)
                //defaults first image color to be darkGray
                iconImageView.tintColor = UIColor.darkGray
            }
        }
    }
    
    let nameLabel: UILabel = {
        let label = UILabel()
        //label.text = "Settings"
        label.font = UIFont.systemFont(ofSize: 14)
        return label
    }()
    
    let iconImageView: UIImageView = {
        let imageView = UIImageView()
        //imageView.image = UIImage(named: "settings_icon")
        imageView.contentMode = .scaleAspectFill
        return imageView
    }()
    
    override func setupViews() {
        super.setupViews()
        
        addSubview(nameLabel)
        addSubview(iconImageView)
        
        // creates height and width of the label in the settings menu
        addConstraintsWithFormat(format: "H:|-8-[v0(30)]-8-[v1]|", views: iconImageView, nameLabel)
        addConstraintsWithFormat(format: "V:|[v0]|", views: nameLabel)
        addConstraintsWithFormat(format: "V:[v0(30)]", views: iconImageView)
        addConstraint(NSLayoutConstraint(item: iconImageView, attribute: .centerY, relatedBy: .equal, toItem: self, attribute: .centerY, multiplier: 1, constant: 0))
    }
}
