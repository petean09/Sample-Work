//
//  SettingsLauncher.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/21/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

// makes a setting object to populate the setting menu cells
class Setting: NSObject {
    let name: SettingName
    let imageName: String
    
    init(name: SettingName, imageName: String) {
        self.name = name
        self.imageName = imageName
    }
}

enum SettingName: String {
    case Logout = "Logout"
    case Settings = "Settings"
    case Request = "Request Event"
    case Profile = "Profile"
    case Info = "Information"
    case Link = "Link to Website"
}

class SettingsLauncher: NSObject, UICollectionViewDataSource, UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    
    let blackView = UIView()
    // must be optional if it doesnt know its nil
    var homeController: HomeController?
    let cellId = "cellId"
    let cellHeight: CGFloat = 50
    
    // creates collectionView to make the settings menu pop up from the bottom
    let collectionView: UICollectionView = {
        let layout = UICollectionViewFlowLayout()
        let cv = UICollectionView(frame: .zero, collectionViewLayout: layout)
        cv .backgroundColor = UIColor.white
        return cv
    }()
    
    // constructing an array to populate setting menu
    let settings: [Setting] = {
        let settingSetting = Setting(name: .Settings, imageName: "settings_icon")
        let logoutSetting = Setting(name: .Logout, imageName: "logout_icon")
        let requestSetting = Setting(name: .Request, imageName: "request_icon")
        let profileSetting = Setting(name: .Profile, imageName: "profile_icon")
        let infoSetting = Setting(name: .Info, imageName: "info_icon")
        let linkSetting = Setting(name: .Link, imageName: "external_link_icon")
        return [settingSetting, requestSetting, profileSetting, infoSetting, linkSetting, logoutSetting]
    }()
    
    //show menu from bottom of screen and add dimmed background animation
    @objc func showSettings() {
        if let window = UIApplication.shared.keyWindow {
            
            // Dim the background to a transparent black
            // creates the transparent black
            blackView.backgroundColor = UIColor(white: 0, alpha: 0.5)
            // On tap black will disappear
            blackView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(handleDismiss)))
            
            window.addSubview(blackView)
            window.addSubview(collectionView)
            
            // specifies how big and where the collectionView (settings menu) is located
            let height: CGFloat = CGFloat(settings.count) * cellHeight
            let y = window.frame.height - height
            collectionView.frame = CGRect(x: 0, y: window.frame.height, width: window.frame.width, height: height)
            
            blackView.frame = window.frame
            blackView.alpha = 0
            
            
            // the black will animate from alpha 0 to alpha 1 and the collectionView will animate up from the bottom
            UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 1, initialSpringVelocity: 1, options: .curveEaseOut, animations: {
                self.blackView.alpha = 1
                self.collectionView.frame = CGRect(x: 0, y: y, width: self.collectionView.frame.width, height: self.collectionView.frame.height)
            }, completion: nil)
        }
    }
    
    // On tap settings menu and black background will disappear
    @objc func handleDismiss(setting: Setting) {
        UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 1, initialSpringVelocity: 1, options: .curveEaseOut, animations: {
            self.blackView.alpha = 0
            if let window = UIApplication.shared.keyWindow {
                self.collectionView.frame = CGRect(x: 0, y: window.frame.height, width: self.collectionView.frame.width, height: self.collectionView.frame.height)
            }
        }) { (completed: Bool) in
            
            if setting.name != .Logout && setting.name != .Link {
                self.homeController?.showControllerForSetting(setting: setting)
            }
        }
    }
    
    //creating cells
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return settings.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: cellId, for: indexPath) as! SettingCell
        
        let setting = settings[indexPath.item]
        cell.setting = setting
        
        return cell
    }
    
    //sizes cells in settings menu
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: collectionView.frame.width, height: cellHeight)
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }

    // This function is executed when an option is clicked in the settings slide-in menu. It creates the animations and lastly calls the function that that gets the next page viewController whatever it may be. (ex.settings  or profile page)
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
        //gets the correct item that was clicked on
        let setting = self.settings[indexPath.item]
        handleDismiss(setting: setting)
    }
    
    override init() {
        super.init()
        
        collectionView.dataSource = self
        collectionView.delegate = self
        
        //register cell
        collectionView.register(SettingCell.self, forCellWithReuseIdentifier: cellId)
    }
}
