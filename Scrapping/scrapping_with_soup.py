from bs4 import BeautifulSoup
import pandas as pd

data=[]

for year in range(2018, 2026):
    with open(f"ipl_{year}_auction.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    tables = soup.find_all("table", class_="table table-hover mb-0")
    table= tables[1]

    def prices_to_float(price):
        price = price.replace("₹", "").replace("â‚¹", "").replace(",", "").strip().lower()
        if "cr" in price:
            return float(price.split(" ")[0]) * 10**7
        elif "l" in price:
            return float(price.split(" ")[0]) * 10**5
        else:
            return float(price.split(" ")[0])

    all_rows= table.find("tbody").find_all("tr")
    for row in all_rows:
        cols = row.find_all("td")
        name= cols[0].find_all("a")[0].text.strip()
        name= " ".join(name.split())
        name=name.replace(",", "").strip()
        team= cols[0].find_all("a")[1].text.strip()
        team= " ".join(team.split())
        price= prices_to_float(cols[1].text.strip().lower())
        
        if "retained" in cols[2].text.strip().lower():
            status= "R"
        elif "unsold" in cols[2].text.strip().lower():
            status= "U"
        else:
            status= "S"
        if price == 0:
            team=""
            status="U"
        if status == "U":
            if "(R)" in name:
                status = "R"
                name.replace("(R)", "").strip()
            else :
                status = "U"
                price = 0
        
        price= price/10**7  # Convert to crores
        data.append({
            "Year": year,
            "Player Name": name,
            "Team Name": team,
            "Price (in crores)": price,
            "Status": status})
auction_data = pd.DataFrame(data)
auction_data.to_csv("ipl_auction_data.csv", index=False)
    
