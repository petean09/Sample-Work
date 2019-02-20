//
//  ViewController.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/7/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit
import EventKit
import Foundation

//struct CalendarPage: Decodable{
//    let vcalendar: [Vcal]
//    struct Vcal: Decodable {
//        let version: String
//        let prodid: String
//        let xwrcalname: String
//        let xwrtimezone: String
//        let vevent: [Events]
//
//        enum CodingKeys : String, CodingKey {
//            case version, prodid, xwrcalname = "x-wr-calname", xwrtimezone = "x-wr-timezone", vevent
//        }
//        struct Events: Decodable {
//            let uid: String?
//            let summary: String?
//            let description: String?
//            let location: String?
//            let created: String?
//            let lastmod: String?
//            let duration: String?
//            let rrule: [Rrule]?
//            struct Rrule: Decodable {
//                let freq: String?
//                let until: String?
//                let interval: String?
//
//            let dstart: ArrayOrString
//            let dtend: StringOrArray
//            }
//
//
////            // dstart and dtend are either strings or arrays... IDK what to do
//            enum ArrayOrString: Decodable {
//                init(from decoder: Decoder) throws {
//                    let container = try decoder.container(keyedBy: CodingKeys.self) //defining the keyed contrainer
//                    if let dstart = try container.decodeIfPResent(String.self, forKey: .dstart) {
//                        let dstart: String
//                    } else {
//                        let dstart: [Start]
//                        struct Start: Decodable {
//                            let value: String?
//                        }
//                    }
//                }
//            }
//
//            enum StringOrArray: Decodable {
//                init(from decoder: Decoder) throws {
//                    let container = try decoder.container(keyedBy: CodingKeys.self) //defining the keyed contrainer
//                    if let dtend = try container.decodeIfPresent(String.self, forKey: .dtend) {
//                        let dtend: String
//                    } else {
//                        let dtend: [End]
//                        struct End: Decodable {
//                            let value: String?
//                        }
//                    }
//
//                }
//
//            }
//
////
//////            extension ArrayOrString: Decodable {
//////                enum CodingKeys: String, CodingKey {
//////                    case dstart, dtend
//////                }
//////            }
////
//////            let dstart: [Start]?
////            struct Start: Decodable {
////                let value: String?
////            }
//////            let dtend: [End]?
////            struct End: Decodable {
////                let value: String?
////            }
//
//
//            enum CodingKeys : String, CodingKey {
//                case uid, summary, description, location, created, lastmod = "last-modified", duration, rrule
//            }
//        }
//
//    }
//
//}


class HomeController: UICollectionViewController, UICollectionViewDelegateFlowLayout{
    
    
//    func fetchEventInfo() {
//        guard let url = URL(string: "http://ical-to-json.herokuapp.com/convert.json?url=https%3A%2F%2Fwww.luther.edu%2Fevents%2F%3Fstart_date%3D2019-01-15%26format%3Dical") else { return }
//
//        URLSession.shared.dataTask(with: url) { (data, response, error) in
//
//            guard let data = data else { return }
//
//            do {
////                let parsed: JSONValue = try JSONDecoder().decode(JSONValue.self, from: data)
////                    print (parsed)
//                let calendar = try JSONDecoder().decode(CalendarPage.self, from: data)
//                print(calendar.vcalendar)
//
//            } catch
//                let jsonErr {
//                    print("Error: ", jsonErr)
//            }
//
//            if error != nil {
//                print(error!)
//                return
//            }
//        }.resume()
    //}
    
    let cellId = "cellId"
    let AthleticCellId = "AthleticCellId"
    let ArtCellId = "ArtCellId"
    let OtherCellId = "OtherCellId"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // attempting to fetch and parse data from website
        //fetchEventInfo()
        
        
        // makes the navigation bar translucent to the color is clearer
        navigationController?.navigationBar.isTranslucent = false
        
        // lefts aligns navbar text, sets to white, fontsize bigger
        let viewWidth = Int(view.bounds.width)
        let viewHeight = Int(view.bounds.height)
        let titleLabel = UILabel(frame: CGRect(x: 0, y: 0, width: viewWidth - 32, height: viewHeight))
        titleLabel.text = "  Events"
        titleLabel.textColor = UIColor.white
        titleLabel.font = UIFont.systemFont(ofSize: 20)
        navigationItem.titleView = titleLabel
        
        // called to set up main collectionView
        setupCollectionView()
        
        // called to set up menubar
         setupMenuBar()
        
        // called to set up navbar buttons
        setupNavBarButtons()
        
    }
    
    // sets up main page
    func setupCollectionView() {
        
        // allows us to access flowlayout from AppDelegate so we can change scroll features
        if let flowLayout = collectionView?.collectionViewLayout as? UICollectionViewFlowLayout {
            // scolling left to right
            flowLayout.scrollDirection = .horizontal
            // minimizes gap between cells so everything is aligned correctly
            flowLayout.minimumLineSpacing = 0
        }
        
        // sets view background to white
        collectionView?.backgroundColor = UIColor.white
        
        // uses a FeedCell (section 1)
        collectionView?.register(FeedCell.self, forCellWithReuseIdentifier: cellId)
        // uses a AthleticsCell (section 2)
        collectionView?.register(AthleticCell.self, forCellWithReuseIdentifier: AthleticCellId)
//        // uses a ArtsCell (section 3)
        collectionView?.register(ArtCell.self, forCellWithReuseIdentifier: ArtCellId)
//        // uses a OthersCell (section 4)
        collectionView?.register(OtherCell.self, forCellWithReuseIdentifier: OtherCellId)
        
        
        // called to update status bar style (white)
        setNeedsStatusBarAppearanceUpdate()
        
        // makes sure feeds start below the menubar and not the navbar (adds 50 pixels to the collectionview)
        collectionView?.contentInset = UIEdgeInsets(top: 50, left: 0, bottom: 0, right: 0)
        // moves scroll bar down 50 pixels as well
        collectionView?.scrollIndicatorInsets = UIEdgeInsets(top: 50, left: 0, bottom: 0, right: 0)
        
        // snaps horizontal scroll into place
        collectionView?.isPagingEnabled = true
        
    }
    
    // sets up navbar buttons
    func setupNavBarButtons() {
        let searchImage = UIImage(named: "search_icon")?.withRenderingMode(.alwaysOriginal)
        let seachBarButtonItem = UIBarButtonItem(image: searchImage, style: .plain, target: self, action: #selector(handleSearch))
        
        let dotImage = UIImage(named: "menu")?.withRenderingMode(.alwaysOriginal)
        let threeDotsButton = UIBarButtonItem(image: dotImage, style: .plain, target: self, action: #selector(handleMore))
        
        
        navigationItem.rightBarButtonItems = [threeDotsButton, seachBarButtonItem]
    }
    
    // show settings menu. Only executed when menu button is clicked the first time due to the lazy var. Without lazy var it would be executed everytime.
    lazy var settingsLauncher: SettingsLauncher = {
        let launcher = SettingsLauncher()
        launcher.homeController = self
        return launcher
    }()
    
    // This is called when the menu button is clicked. This function call all other functions to work and create the menu.
    @objc func handleMore() {
        settingsLauncher.showSettings()
        }
    
    // This function creates the new pages when any item on the settings menu is clicked. ViewControllers are created.
    func showControllerForSetting(setting: Setting) {
        let dummySettingsViewController = UIViewController()
        //background turns white
        dummySettingsViewController.view.backgroundColor = UIColor.white
        dummySettingsViewController.navigationItem.title = setting.name.rawValue
        //back button turns white
        navigationController?.navigationBar.tintColor = UIColor.white
        //middle title turns white
        navigationController?.navigationBar.titleTextAttributes = [NSAttributedString.Key.foregroundColor: UIColor.white]
        navigationController?.pushViewController(dummySettingsViewController, animated: true)
    }
    
    let searchBarHeight: CGFloat = 40
    
    @objc func handleSearch() {
        let searchBar = UISearchBar(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: searchBarHeight))
        searchBar.sizeToFit()
        searchBar.placeholder = "Search Events"
        view.addSubview(searchBar)
    }
    
    func scrollToMenuIndex(menuIndex: Int) {
        let indexPath = NSIndexPath(item: menuIndex, section: 0)
        collectionView?.scrollToItem(at: indexPath as IndexPath, at: .centeredHorizontally, animated: true)
    }
    
    // next ten lines set up menubar
    // lazy var used to make self accessable in this block
    lazy var menuBar: MenuBar = {
        let mb = MenuBar()
        mb.homeController = self
        return mb
    }()
    
    private func setupMenuBar() {
        // navigation bar will hide up when scrolling
        navigationController?.hidesBarsOnSwipe = true
        
        // there was a gap below the bar on top when scrolling so a blue background was added behind the menubar
        let blueView = UIView()
        blueView.backgroundColor = UIColor.blue
        view.addSubview(blueView)
        view.addConstraintsWithFormat(format: "H:|[v0]|", views: blueView)
        view.addConstraintsWithFormat(format: "V:[v0(50)]", views: blueView)
        
        view.addSubview(menuBar)
        view.addConstraintsWithFormat(format: "H:|[v0]|", views: menuBar)
        view.addConstraintsWithFormat(format: "V:[v0(50)]", views: menuBar)
        
        // Holds the menuBar to the top most portion of the view of the window so when scrolling it looks right
        menuBar.topAnchor.constraint(equalTo: topLayoutGuide.bottomAnchor).isActive = true
    }
    
    // Finds out where the location of the scroll is
    // Moves the small white bar with the scrolling
    // divided by 4 becuase 4 menuBar sections
    override func scrollViewDidScroll(_ scrollView: UIScrollView) {
        menuBar.horizontalBarLeftAnchorConstraint?.constant = scrollView.contentOffset.x / 4
    }
    
    // finds target location so when the pages are scrolled horizontally the section buttons (all,athl,arts,other) turn black indicating they are on that page
    override func scrollViewWillEndDragging(_ scrollView: UIScrollView, withVelocity velocity: CGPoint, targetContentOffset: UnsafeMutablePointer<CGPoint>) {
        
        
        let index = targetContentOffset.pointee.x / view.frame.width
        
        let indexPath = NSIndexPath(item: Int(index), section: 0)
        menuBar.collectionView.selectItem(at: indexPath as IndexPath, animated: true, scrollPosition: [])
    }

    // makes 4 sections
    override func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 4
    }
    
    // shows 4 sections
    override func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell
            {
                
            // renders the different event feeds
            let identifier: String
            if indexPath.item == 1 {
                identifier = AthleticCellId
            } else if indexPath.item == 2 {
                identifier = ArtCellId
            } else if indexPath.item == 3 {
                identifier = OtherCellId
            } else {
                identifier = cellId
                }
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: identifier, for: indexPath)
            return cell
        }
    
    // sizes sections
    // subtract 50 pixels becuase of menubar
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: view.frame.width, height: view.frame.height - 50)
    }
}








