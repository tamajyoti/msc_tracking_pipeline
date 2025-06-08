tables = {
    "bill_of_lading": {
        "name": "bill_of_lading",
        "schema": """
            Id TEXT PRIMARY KEY,
            TrackingType TEXT,
            TrackingNumber TEXT,
            NumberOfContainers INTEGER,
            BillOfLadingNumber TEXT,
            ShippedFrom TEXT,
            ShippedTo TEXT,
            PortOfLoad TEXT,
            PortOfDischarge TEXT,
            PriceCalculationDate TEXT,
            FinalPodEtaDate TEXT
        """,
        "primary_key": "Id"
    },
    "containers": {
        "name": "containers",
        "schema": """
            Id TEXT PRIMARY KEY,
            TrackingType TEXT,
            TrackingNumber TEXT,
            BillOfLadingNumber TEXT,
            ShippedFrom TEXT,
            ShippedTo TEXT,
            PortOfLoad TEXT,
            PortOfDischarge TEXT,
            PriceCalculationDate TEXT,
            FinalPodEtaDate TEXT,
            OrderNo INTEGER,
            Date TEXT,
            Location TEXT,
            Description TEXT,
            ContainerNumber TEXT,
            Delivered BOOLEAN,
            PodEtaDate TEXT,
            ContainerType TEXT,
            LatestMove TEXT
        """,
        "primary_key": "Id"
    }
}