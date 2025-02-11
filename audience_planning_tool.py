import { useState } from "react";
import { Input, Select, Button } from "@/components/ui";
import { Card, CardContent } from "@/components/ui/card";
import { MapPin } from "lucide-react";
import dynamic from "next/dynamic";

const Map = dynamic(() => import("@/components/Map"), { ssr: false });

export default function AudiencePlanner() {
  const [regionType, setRegionType] = useState("National");
  const [filters, setFilters] = useState({
    income: "",
    housePrice: "",
    language: "",
  });
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    // Fetch relevant zip codes from a backend service that scrapes and aggregates web data
    const response = await fetch("/api/getZipCodes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ regionType, filters }),
    });
    const data = await response.json();
    setResults(data.zipCodes);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Audience Planning Tool</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Select value={regionType} onChange={(e) => setRegionType(e.target.value)}>
          <option value="National">National</option>
          <option value="State">State</option>
          <option value="DMA">DMA</option>
        </Select>
        <Input
          type="text"
          placeholder="Household Income ($)"
          value={filters.income}
          onChange={(e) => setFilters({ ...filters, income: e.target.value })}
        />
        <Input
          type="text"
          placeholder="Average House Price ($)"
          value={filters.housePrice}
          onChange={(e) => setFilters({ ...filters, housePrice: e.target.value })}
        />
        <Input
          type="text"
          placeholder="Language Spoken"
          value={filters.language}
          onChange={(e) => setFilters({ ...filters, language: e.target.value })}
        />
      </div>
      <Button className="mt-4" onClick={handleSearch}>Find Zip Codes</Button>
      <div className="mt-6">
        {results.map((zip) => (
          <Card key={zip} className="mb-2 flex items-center gap-3 p-4">
            <MapPin className="text-blue-500" />
            <CardContent>{zip}</CardContent>
          </Card>
        ))}
      </div>
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Zip Codes Map</h2>
        <Map zipCodes={results} />
      </div>
    </div>
  );
}
